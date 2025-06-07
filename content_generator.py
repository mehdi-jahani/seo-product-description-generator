import requests
import torch
import re
import logging
from config import HF_TOKEN, MODEL_NAME, VLLM_API_URL, USE_VLLM
from transformers import AutoTokenizer, AutoModelForCausalLM

# --------------------------
# Logging Setup
# --------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler('app.log'), logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

# --------------------------
# Prompt Builder
# --------------------------
def build_prompt(product):
    return f"""
You are a professional eCommerce copywriter and SEO strategist with deep experience in crafting high-converting, benefit-driven product descriptions for online stores.

Your task is to generate a product description broken into **4 clearly defined sections**, using a persuasive and friendly tone that connects with potential buyers.

Here are the product details:
- **Product Title**: {product['title']}
- **Category**: {product['category']}
- **Key Features**: {product['features']}
- **Price**: ${product['price']}

Please write the following sections:

1. **What Makes It Special** – A short paragraph that introduces the product and highlights what makes it unique.
2. **Why You'll Love It** – Emphasize key benefits and emotional triggers that resonate with buyers.
3. **Perfect For** – Clearly describe the ideal user, use case, or lifestyle fit for the product.
4. **Call to Action** – End with a persuasive and energetic sentence that encourages immediate action.

Guidelines:
- Each section should be 8–12 sentences long.
- Use natural language that includes relevant SEO keywords such as "{product['title']}", "{product['category']}", and notable features.
- Avoid clichés and focus on original, conversion-driven content.
- Do **not** return a single paragraph — break the output clearly into the 4 sections with proper headings.

Output the final result in plain text. Do not include explanations or notes.
"""

# --------------------------
# Model Initialization
# --------------------------
if not USE_VLLM:
    logger.info("Loading local model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=HF_TOKEN)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float16,
        device_map="auto",
        token=HF_TOKEN
    )
    try:
        model = torch.compile(model)
        logger.info("Model compiled successfully.")
    except Exception as e:
        logger.warning(f"Model compilation skipped: {e}")

# --------------------------
# Description Parser
# --------------------------
def parse_description_to_sections(text):
    sections = {
        "section1": "",
        "section2": "",
        "section3": "",
        "cta": ""
    }

    # Normalize line breaks
    text = re.sub(r'\r\n|\r', '\n', text)
    text = re.sub(r'\n{2,}', '\n', text)

    patterns = {
        "section1": r"What Makes It Special[\?:]?\s*(.+?)(?=\n\s*Why You'll Love It|$)",
        "section2": r"Why You'll Love It\s*(.+?)(?=\n\s*Perfect For|$)",
        "section3": r"Perfect For\s*(.+?)(?=\n\s*Call to Action|$)",
        "cta": r"Call to Action\s*(.+)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            sections[key] = match.group(1).strip()
        else:
            logger.warning(f"Section '{key}' not found in generated text.")

    return sections

# --------------------------
# Description Generator
# --------------------------
def generate_description(product):
    prompt = build_prompt(product)
    logger.info(f"Generating description for product: {product['title']}")

    if USE_VLLM:
        logger.info("Using VLLM API for generation...")
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 800,
            "temperature": 0.7,
            "top_p": 0.95
        }
        try:
            response = requests.post(VLLM_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            output_text = result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logger.error(f"Error calling VLLM API: {e}")
            return None
    else:
        logger.info("Generating locally using HuggingFace model...")
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

        with torch.autocast("cuda"):
            outputs = model.generate(
                **inputs,
                max_new_tokens=1200,
                temperature=0.7,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id
            )

        decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
        output_text = decoded.split(prompt)[-1].strip()

    logger.debug("Generated raw output:\n" + output_text[:500])  # Print first 500 characters

    return parse_description_to_sections(output_text)

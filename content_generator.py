from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from config import MODEL_NAME

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    torch_dtype=torch.float16
)

def generate_description(product):
    prompt = f"""You are a professional product copywriter.

Write an SEO-optimized and persuasive product description for:
Title: {product['title']}
Category: {product['category']}
Key Features: {product['features']}
Price: ${product['price']}

Use friendly and clear English, include benefits and a call to action.
"""
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=50,
        temperature=0.7,
        do_sample=True,
        top_k=50,
        top_p=0.95
    )
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return result.split(prompt)[-1].strip()

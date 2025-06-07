# Model config
MODEL_NAME = "NousResearch/Nous-Hermes-2-Mistral-7B-DPO"
HF_TOKEN = "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"

# Input/output
INPUT_FILE = "data/products.csv"
OUTPUT_DIR = "outputs"

# Language setting
LANGUAGE = "en"  # Future-proofing for multilingual support

# vLLM API config
VLLM_API_URL = "http://localhost:8000/v1/chat/completions"
USE_VLLM = False  # If set to True, will use vLLM API instead of local transformers

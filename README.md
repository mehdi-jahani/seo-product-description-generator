
# 🧠 SEO Content Generator

A powerful and customizable AI-based product description generator built for eCommerce platforms. This tool crafts SEO-optimized, high-converting product descriptions using cutting-edge language models (e.g. Hugging Face Transformers or vLLM APIs).

## 🚀 Features

- ✅ Generates product descriptions in 4 persuasive sections:
  - What Makes It Special
  - Why You'll Love It
  - Perfect For
  - Call to Action
- 🎯 Optimized for SEO and conversion
- 📦 Supports local HuggingFace models and remote vLLM APIs
- 🔍 Structured prompt design for consistent output
- 📝 HTML output templates for easy integration into websites
- ⚙️ Modular design with configuration flexibility

## 🛠 Requirements

- Python 3.8+
- pip

Install dependencies:

```bash
pip install -r requirements.txt
```

## 📂 Project Structure

```
seo_content_generator/
├── config.py               # Configuration for model, tokens, and settings
├── content_generator.py    # Main logic for prompt generation and parsing
├── input_handler.py        # Handles product input data
├── output_writer.py        # Writes HTML output using templates
├── main.py                 # Entry point for running the tool
├── templates/              # HTML templates
├── outputs/                # Generated HTML files
```

## 🧪 Usage

```bash
python main.py
```

You can configure:
- Your HuggingFace model or vLLM endpoint via `config.py`
- Input products as Python dictionaries or JSON
- HTML template in `templates/base_template.txt`

## 🖼 Example Output

A single product input will generate an SEO-rich description like this:

```
✨ What Makes It Special?
Experience wireless freedom and unmatched sound quality with our Bluetooth Headphones...

🚀 Why You'll Love It
Whether you're commuting or relaxing, enjoy 20hr battery life, active noise cancelation...

🎯 Perfect For
Designed for music lovers, remote workers, and frequent travelers...

🛒 Call to Action
Don’t wait – upgrade your listening experience today!
```

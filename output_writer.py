import os

def write_html_output(product, description_parts, output_dir="outputs", template_path="templates/base_template.txt"):
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{product['id']}_{product['title'].replace(' ', '_')}.html"
    filepath = os.path.join(output_dir, filename)

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    features_html = "\n".join(f"<li>{f.strip()}</li>" for f in product['features'].split(','))

    html = template \
        .replace("{{title}}", product['title']) \
        .replace("{{category}}", product['category']) \
        .replace("{{features}}", features_html) \
        .replace("{{price}}", str(product['price'])) \
        .replace("{{body_section_1}}", description_parts.get("section1", "")) \
        .replace("{{body_section_2}}", description_parts.get("section2", "")) \
        .replace("{{body_section_3}}", description_parts.get("section3", "")) \
        .replace("{{cta}}", description_parts.get("cta", "Click Add to Cart now and experience the difference!"))

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

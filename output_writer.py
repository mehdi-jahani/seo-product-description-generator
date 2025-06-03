import os

def write_html_output(product, description, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{product['id']}_{product['title'].replace(' ', '_')}.html"
    filepath = os.path.join(output_dir, filename)

    html = f"""
    <html>
    <head><title>{product['title']}</title></head>
    <body>
        <h1>{product['title']}</h1>
        <h3>Category: {product['category']}</h3>
        <ul>
            {''.join(f"<li>{f.strip()}</li>" for f in product['features'].split(','))}
        </ul>
        <p><strong>Price:</strong> ${product['price']}</p>
        <p>{description}</p>
    </body>
    </html>
    """

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

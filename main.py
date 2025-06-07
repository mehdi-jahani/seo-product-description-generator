from config import INPUT_FILE, OUTPUT_DIR
from input_handler import load_products_from_csv
from content_generator import generate_description
from output_writer import write_html_output

def main():
    products = load_products_from_csv(INPUT_FILE)

    for product in products:
        print(f"Generating description for: {product['title']}")
        sections = generate_description(product)
        write_html_output(product, sections, OUTPUT_DIR)

    print("✅ Content generation and HTML saving completed successfully.")

if __name__ == "__main__":
    main()

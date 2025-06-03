from config import INPUT_FILE, OUTPUT_DIR
from input_handler import load_products_from_csv
from content_generator import generate_description
from output_writer import write_html_output

def main():
    products = load_products_from_csv(INPUT_FILE)

    for product in products:
        print(f"Generating description for: {product['title']}")
        description = generate_description(product)
        write_html_output(product, description, OUTPUT_DIR)

    print("✅ تولید محتوا و ذخیره HTML با موفقیت انجام شد.")

if __name__ == "__main__":
    main()

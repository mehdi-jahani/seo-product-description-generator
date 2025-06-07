import csv

def load_products_from_csv(file_path):
    products = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Optional: Strip leading/trailing whitespaces
            cleaned_row = {k: v.strip() if isinstance(v, str) else v for k, v in row.items()}
            products.append(cleaned_row)
    return products

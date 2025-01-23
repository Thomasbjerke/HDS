import requests

class ShopifyProductUploader:
    def __init__(self, shopify_access_token, shopify_store_name):
        self.access_token = shopify_access_token
        self.store_name = shopify_store_name
        self.base_url = f"https://{self.store_name}.myshopify.com/admin/api/2023-01"

    def create_product(self, product_name, image_url, price):
        product_endpoint = f"{self.base_url}/products.json"
        headers = {
            "X-Shopify-Access-Token": self.access_token,
            "Content-Type": "application/json"
        }
        payload = {
            "product": {
                "title": product_name,
                "body_html": "High-quality digital art print.",
                "images": [{"src": image_url}],
                "variants": [{"price": price, "sku": "ART-001"}]
            }
        }
        response = requests.post(product_endpoint, headers=headers, json=payload)
        if response.status_code == 201:
            print("Product created successfully in Shopify!")
            return response.json()["product"]["id"]
        else:
            print("Error creating product in Shopify:", response.json())
            return None

# Usage
SHOPIFY_ACCESS_TOKEN = "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"
SHOPIFY_STORE_NAME = "egqhfk-mc"  # Replace with your Shopify store name
PRODUCT_NAME = "Digital Art Print"
IMAGE_URL = "https://storagehds.blob.core.windows.net/processed-images/2. Grand Hotel_art.jpg"
PRICE = "99.00"

shopify_uploader = ShopifyProductUploader(SHOPIFY_ACCESS_TOKEN, SHOPIFY_STORE_NAME)
shopify_uploader.create_product(PRODUCT_NAME, IMAGE_URL, PRICE)

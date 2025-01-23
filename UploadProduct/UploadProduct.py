import requests

class UploadProduct:
    def __init__(self, access_token, store_id):
        self.access_token = access_token
        self.store_id = store_id
        self.base_url = "https://api.printful.com"

    def upload_artwork(self, image_url):
        # Endpoint to upload files with store_id
        upload_endpoint = f"{self.base_url}/files?store_id={self.store_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {"url": image_url}

        response = requests.post(upload_endpoint, headers=headers, json=payload)

        if response.status_code == 200:
            print("File uploaded successfully!")
            file_id = response.json()["result"]["id"]
            return file_id
        else:
            print("Error uploading file:", response.json())
            return None

    def create_product(self, file_id, product_name, variant_id, retail_price):
        # Endpoint to create a product
        product_endpoint = f"{self.base_url}/store/products?store_id={self.store_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "sync_product": {
                "name": product_name,
                "thumbnail": f"{self.base_url}/files/{file_id}"
            },
            "sync_variants": [
                {
                    "retail_price": retail_price,
                    "variant_id": variant_id,
                    "files": [{"type": "front", "id": file_id}]
                }
            ]
        }

        response = requests.post(product_endpoint, headers=headers, json=payload)

        if response.status_code == 200:
            print("Product created successfully!")
        else:
            print("Error creating product:", response.json())

# Usage
if __name__ == "__main__":
    # Replace with your actual access token and store ID
    ACCESS_TOKEN = "DJMgHKKdvbTKbBWdudKWaHgJDXz0JASApNxMhShr"
    STORE_ID = "15341182"  # Replace with your Printful store ID
    IMAGE_URL = "https://storagehds.blob.core.windows.net/processed-images/2. Grand Hotel_art.jpg"
    PRODUCT_NAME = "Digital Art Print"
    VARIANT_ID = 52355445129587  # Example variant ID
    RETAIL_PRICE = "99.00"

    uploader = UploadProduct(ACCESS_TOKEN, STORE_ID)
    file_id = uploader.upload_artwork(IMAGE_URL)
    if file_id:
        uploader.create_product(file_id, PRODUCT_NAME, VARIANT_ID, RETAIL_PRICE)

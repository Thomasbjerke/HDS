import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from AskAI.AskAI import AskAI
from ImageSearch.ImageSearch import ImageSearch
from Img2Img.Img2Img import Img2Img
import json
import os

# Initialize your classes
openai_api_key = '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'
phi_api_key = 'hdTsphcX6deWaETLURkdfejyqAClfrZU'
phi_api_endpoint = 'https://Phi-3-5-vision-instruct-ulhdg.swedencentral.models.ai.azure.com/v1/chat/completions'
ask_ai = AskAI(openai_api_key, phi_api_key, phi_api_endpoint)

image_search = ImageSearch(api_key="6484654a6e0b47998c8f32ccaf88a4b4")
img2img = Img2Img()  # Ensure you pass API details

def main(bildeTimer: func.TimerRequest) -> None:
    logging.info('Function B is starting...')
    
    connection_string = "DefaultEndpointsProtocol=https;AccountName=storagehds;AccountKey=ZDn4sWoJ2Cx//VNls9RhvryfA3yybwxNxd0OjSS1vDK/CnIeJrLA1/oMo0OemH/uY5uc2NsndI/n+AStQcKzDg==;EndpointSuffix=core.windows.net"
    
    # Set up Blob Storage client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    # Retrieve the current hotel list from Blob Storage
    container_name = "hotellist"
    blob_name = "hotels.json"
    
    try:
        blob_client = blob_service_client.get_blob_client(container_name, blob_name)
        hotels_json = blob_client.download_blob().readall()
        hotels = json.loads(hotels_json)
        logging.info("Successfully retrieved the existing hotel list.")
    except Exception as e:
        if 'BlobNotFound' in str(e):
            logging.info("The hotels.json blob does not exist, initializing an empty list.")
            hotels = []  # Start with an empty list if blob doesn't exist
        else:
            logging.error(f"Error retrieving hotel list: {e}")
            return  # Stop execution if there's a different error

    # Get the next 6 unprocessed hotels
    hotels_to_process = [hotel for hotel in hotels if not hotel.get('processed', False)][:6]

    if not hotels_to_process:
        logging.info("No unprocessed hotels found.")
        return

    for hotel in hotels_to_process:
        logging.info(f"Processing hotel: {hotel['name']}")

        # Step 1: Search and download the first 10 exterior image URLs
        image_urls = image_search.get_first_image_urls(hotel['name'] + " " + hotel['location'], num_urls=10)

        found_exterior = False

        # Step 2: Check for exterior image
        for image_url in image_urls:
            logging.info(f"Url: {image_url}")
            if str(ask_ai.check_if_exterior(image_url)).strip() == "Yes":
                # Generate digital art based on the exterior image
                try:
                    generated_image_data = img2img.generate_image(image_url, "Cartoon")
                    # Save the generated image to Blob Storage
                    processed_blob_client = blob_service_client.get_blob_client("processed-images", f"{hotel['name']}_art.jpg")
                    processed_blob_client.upload_blob(generated_image_data, overwrite=True)
                    logging.info(f"Generated art for {hotel['name']} saved to Blob Storage.")
                except Exception as e:
                    logging.error(f"Error generating or uploading art for {hotel['name']}: {e}")
                found_exterior = True
                break

        # Step 3: Handle case where no exterior image is found
        if not found_exterior:
            logging.warning(f"No exterior image found for {hotel['name']}. Marking for review.")
            hotel['needs_review'] = True  # Mark the hotel for later review
            continue  # Skip further processing for this hotel

        # Mark the hotel as processed
        hotel['processed'] = True

    # Upload the updated list back to Blob Storage
    try:
        blob_client.upload_blob(json.dumps(hotels), overwrite=True)
        logging.info("Updated hotel list saved to Blob Storage.")
    except Exception as e:
        logging.error(f"Error uploading updated hotel list: {e}")

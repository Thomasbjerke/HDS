import logging
import azure.functions as func
from AskAI.AskAI import AskAI
from azure.storage.blob import BlobServiceClient
import json

# Initialize your class
openai_api_key = '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'
phi_api_key = 'hdTsphcX6deWaETLURkdfejyqAClfrZU'
phi_api_endpoint = 'https://Phi-3-5-vision-instruct-ulhdg.swedencentral.models.ai.azure.com/v1/chat/completions'
ask_ai = AskAI(openai_api_key, phi_api_key, phi_api_endpoint)

def main(listeTimer: func.TimerRequest) -> None:
    logging.info('Function A is starting...')

    connection_string = "DefaultEndpointsProtocol=https;AccountName=storagehds;AccountKey=ZDn4sWoJ2Cx//VNls9RhvryfA3yybwxNxd0OjSS1vDK/CnIeJrLA1/oMo0OemH/uY5uc2NsndI/n+AStQcKzDg==;EndpointSuffix=core.windows.net"
    
    # Convert the list to JSON and save to Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_name = "hotellist"
    blob_name = "hotels.json"
    
    container_client = blob_service_client.get_container_client(container_name)

    # Download the existing hotel list from blob storage
    try:
        blob_client = container_client.get_blob_client(blob_name)
        hotels_json = blob_client.download_blob().readall()
        current_hotels = json.loads(hotels_json)
        logging.info("Successfully retrieved the existing hotel list.")
    except Exception as e:
        if 'BlobNotFound' in str(e):
            logging.info("The hotels.json blob does not exist, initializing an empty list.")
            current_hotels = []  # Start with an empty list if blob doesn't exist
        else:
            logging.error(f"Error retrieving hotel list: {e}")
            return  # Stop execution if there's a different error

    # Generate a new list of 100 hotels, ensuring no duplicates with current list
    new_hotels = ask_ai.get_list_of_hotels('Norway', current_hotels)

    # Combine the current list with the new hotels
    updated_hotel_list = current_hotels + new_hotels

    # Upload the updated list back to Blob Storage
    try:
        blob_client.upload_blob(json.dumps(updated_hotel_list), overwrite=True)
        logging.info('Updated hotel list saved to Blob Storage.')
    except Exception as e:
        logging.error(f"Error uploading updated hotel list: {e}")


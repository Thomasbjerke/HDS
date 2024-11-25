import openai
import requests
from openai import OpenAI

class AskAI:
    def __init__(self, openai_api_key, phi_api_key, phi_api_endpoint):
        # Initialize API keys and endpoints
        self.openai_api_key = openai_api_key
        self.phi_api_key = phi_api_key
        self.phi_api_endpoint = phi_api_endpoint
        
        # Set up OpenAI API client
        self.client = OpenAI(api_key=self.openai_api_key)
        
        # Set up OpenAI API key for requests
        openai.api_key = self.phi_api_key
    
    def get_list_of_hotels(self, country, current_hotel_list):
        # Call OpenAI API to get a list of hotels
        completion = self.client.chat.completions.create(
            model="gpt-4o",  # Adjust the model name as necessary
            messages=[
                {"role": "system", "content": "You find real hotels based on criteria given by the user. Answer only with a list of real hotels in the format 'Hotel Name, Location', nothing else. It is important that you only use hotels that actually exist, and always include the location in case it's important to distinguish between hotels with the same name in different cities."},
                {"role": "user", "content": "Give me a list of 100 venerable hotels that actually exist in " + country + ". Do not include any of the following hotels: " + str(current_hotel_list)}
            ]
        )

        # Parse the returned text into a list of dictionaries
        hotels_text = completion.choices[0].message.content.strip().split("\n")
        
        # Convert the list of hotel strings into a list of dictionaries with 'name' and 'location'
        hotels = []
        for hotel_text in hotels_text:
            if "," in hotel_text:
                name, location = hotel_text.split(",", 1)
                hotels.append({"name": name.strip(), "location": location.strip()})

        return hotels

    
    def get_email_address(self, hotel_name):
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",  # Adjust the model name as necessary
            messages=[
                {"role": "system", "content": "You find email addresses that can be used for business inquiries for specific hotels. Answer only with a the email address, nothing else. Do not start your answer with 'Sure' or anything like that, go straight to the list. If you can not find an email address specifically for business inquiries, return the most relevant email address you can find for the hotel."},
                {"role": "user", "content": "I have a business inquiry. Give me the email address i should use to contact" + hotel_name + "."}
            ]
        )
        return completion.choices[0].message.content

    
    def check_if_exterior(self, image_url):
        # Prepare the request payload for checking if the image is an exterior view
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are an assistant that checks whether images depict the outside of buildings. Answer all questions with either 'Yes' or 'No'."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Does this image show the outside of a building, and is the entire building visible without being cut off at all? Answer 'Yes' only if both are true, otherwise answer 'No.'"},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ],
            "max_tokens": 100  # Adjust token limit as needed
        }

        # Set the headers with Authorization as required
        headers = {
            "Authorization": f"Bearer {self.phi_api_key}",  # Use 'Bearer' prefix
            "Content-Type": "application/json"  # Set the content type to JSON
        }

        # Send the request to the Azure OpenAI API
        response = requests.post(self.phi_api_endpoint, json=payload, headers=headers)

        # Process and return the response
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"Request failed: {response.status_code}, {response.text}"

# Example usage
if __name__ == "__main__":
    openai_api_key = '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'
    phi_api_key = 'hdTsphcX6deWaETLURkdfejyqAClfrZU'
    phi_api_endpoint = 'https://Phi-3-5-vision-instruct-ulhdg.swedencentral.models.ai.azure.com/v1/chat/completions'
    image_url = 'https://smllighting.no/wp-content/uploads/2020/12/DSC0218-Edit.jpg'

    AskAI = AskAI(openai_api_key, phi_api_key, phi_api_endpoint)

    # Get list of hotels
    #print(AskAI.get_list_of_hotels("Norway"))

    # Check if the image shows an exterior
    test = AskAI.check_if_exterior(image_url)
    if str(test).strip() == "Yes":
        print("Yes")

    else:
        print("Nei: ", str(test))

    #print(AskAI.get_email_address("Hotel Brosundet"))

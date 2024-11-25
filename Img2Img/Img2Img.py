import requests
import base64
import os

class Img2Img:
    def __init__(self, api_key="key-ccnHdLoNVLaQPvngYlKxqeXK2cgiiLUKNaDUTpc6eXRmAlLE4c7aR1qLKcM4W5ow3AliGIC2agk6VvtMMxYLIr9HVsaM8WL", endpoint="https://api.getimg.ai/v1/stable-diffusion/image-to-image"):
        self.api_key = api_key
        self.endpoint = endpoint

    def generate_image(self, input_image_url, prompt):
        # Download the input image from the provided URL
        response = requests.get(input_image_url)
        if response.status_code != 200:
            raise Exception(f"Failed to download input image from {input_image_url}")
        
        # Encode the image as Base64 for the API request
        image_base64 = base64.b64encode(response.content).decode('utf-8')

        # Define the parameters for the image generation request
        data = {
            'model': 'van-gogh-diffusion',  # Example model, adjust as needed
            'prompt': prompt,
            'num_inference_steps': 25,
            'guidance_scale': 7,
            'image': image_base64
        }

        # Set the headers for the request
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        # Make the API call
        response = requests.post(self.endpoint, headers=headers, json=data)
        if response.status_code != 200:
            raise Exception(f"Failed to generate image: {response.status_code} {response.text}")

        # Decode the generated image from the response
        response_data = response.json()
        if 'image' not in response_data:
            raise Exception("Failed to retrieve generated image")

        image_data = base64.b64decode(response_data['image'])

        return image_data  # Return the binary image data

import requests

class ImageSearch:
    def __init__(self, api_key):
        self.api_key = api_key
        self.search_url = "https://api.bing.microsoft.com/v7.0/images/search"
        self.headers = {"Ocp-Apim-Subscription-Key": self.api_key}

    def get_first_image_urls(self, query, num_urls=10):
        params = {"q": query + " utside", "count": num_urls}

        # Make the request to Bing Image Search API
        response = requests.get(self.search_url, headers=self.headers, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        search_results = response.json()

        # Extract and return the first 'num_urls' image URLs if available
        if search_results.get("value"):
            return [image["contentUrl"] for image in search_results["value"][:num_urls]]

        return []

# Example usage
api_key = "6484654a6e0b47998c8f32ccaf88a4b4"
image_search = ImageSearch(api_key)

# Search for a hotel name and get the first 10 exterior image URLs
hotel_name = "Hotel Union Øye"
image_urls = image_search.get_first_image_urls(hotel_name, num_urls=10)

# Print the first 10 image URLs
for idx, url in enumerate(image_urls, 1):
    print(url)





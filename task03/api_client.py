import requests

class APIClient:
    def get_image_url(self, api_type: str) -> str:
        if api_type == "dog":
            response = requests.get("https://dog.ceo/api/breeds/image/random")
            return response.json().get("message")
        
        elif api_type == "cat":
            response = requests.get("https://api.thecatapi.com/v1/images/search")
            return response.json()[0].get("url")
            
        elif api_type == "fox":
            response = requests.get("https://randomfox.ca/floof/")
            return response.json().get("image")
        
        return ""
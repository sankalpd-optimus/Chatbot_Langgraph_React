import requests
import os

class BingSearchRetriever:
    def __init__(self):
        self.endpoint = "https://api.bing.microsoft.com/v7.0/search"
        self.api_key = "your-bing-api-key"

    def invoke(self, query: str) -> str:
        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        params = {"q": query, "count": 5, "textDecorations": True, "textFormat": "HTML"}

        try:
            response = requests.get(self.endpoint, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            search_results = data.get("webPages", {}).get("value", [])

            return "\n".join([result["snippet"] for result in search_results]) if search_results else "No relevant web results found."

        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"  

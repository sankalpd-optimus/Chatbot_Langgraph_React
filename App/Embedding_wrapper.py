import openai
from dotenv import load_dotenv
import os

load_dotenv()

AZURE_API_ENDPOINT = os.getenv("AZURE_API_ENDPOINT")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
AZURE_EMBEDDING_MODEL_KEY=os.getenv("AZURE_EMBEDDING_MODEL_KEY")
AZURE_EMBEDDING_MODEL_NAME=os.getenv("AZURE_EMBEDDING_MODEL_NAME")
AZURE_EMBEDDING_MODEL_ENDPOINT=os.getenv("AZURE_EMBEDDING_MODEL_ENDPOINT")

client = openai.AzureOpenAI(
    api_key=AZURE_EMBEDDING_MODEL_KEY,
    api_version=AZURE_API_VERSION,
    azure_endpoint=AZURE_EMBEDDING_MODEL_ENDPOINT,
    azure_deployment=AZURE_EMBEDDING_MODEL_NAME
)

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",  
        input=[text]
    )
    return response.data[0].embedding

# Test function
if __name__ == "__main__":
    sample_text = "Azure Cosmos DB is a NoSQL database."
    embedding = get_embedding(sample_text)
    print("Embedding generated:", embedding[:5])



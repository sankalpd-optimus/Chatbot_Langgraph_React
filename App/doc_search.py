# stores embeddings of user query and retrieves relevant documents based on cosine similarity
import os
import uuid
import numpy as np
from azure.cosmos import CosmosClient
from dotenv import load_dotenv
from Embedding_wrapper import get_embedding

load_dotenv()

COSMOS_DB_URL = os.getenv("COSMOS_DB_URL")
COSMOS_DB_KEY = os.getenv("COSMOS_DB_KEY")
COSMOS_DB_DATABASE = os.getenv("COSMOS_DB_DATABASE")
COSMOS_DB_CONTAINER = os.getenv("COSMOS_DB_CONTAINER")

client = CosmosClient(COSMOS_DB_URL, credential=COSMOS_DB_KEY)
database = client.get_database_client(COSMOS_DB_DATABASE)
container = database.get_container_client(COSMOS_DB_CONTAINER)

class GetDocSearchResultsTool:
    def __init__(self, k=10):
        self.k = k  # Number of results to return

    def invoke(self, query: str):
        results = self._retrieve_similar_chunks(query)  # Retrieve matching documents

        if not results:
            return "No relevant documents found."

        # Extract text from results
        retrieved_texts = [str(doc[0]) for doc in results]  
        print(f"Retrieved {len(results)} results for query: {query}")
        return " ".join(retrieved_texts)  



    def _retrieve_similar_chunks(self, query):
        #Retrieve similar chunks based on cosine similarity of query embedding
        query_embedding = get_embedding(query)
        documents = list(container.read_all_items())

        similarities = []
        for doc in documents:
            stored_embedding = np.array(doc["embedding"])
            similarity_score = np.dot(query_embedding, stored_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(stored_embedding)
            )
            similarities.append((doc["text"], similarity_score))

        sorted_chunks = sorted(similarities, key=lambda x: x[1], reverse=True)[:self.k]
        return "\n\n".join([chunk[0] for chunk in sorted_chunks]) if sorted_chunks else "No relevant documents found."
def store_embedding(doc_id, text, embedding):
    #Store document embeddings in Cosmos DB.
    document = {
        "id": doc_id,  
        "text": text,
        "embedding": embedding
    }
    container.upsert_item(document)
    print(f"Stored document chunk '{doc_id}' in Cosmos DB.")

def store_query_embedding(query):
    #Store the user query embedding in Cosmos DB
    embedding = get_embedding(query)
    document = {
        "id": str(uuid.uuid4()),  # Generate unique ID
        "text": query,
        "embedding": embedding
    }
    container.upsert_item(document)
    print(f"Stored query '{query}' in Cosmos DB.")

#function call
def run_query_search(query):
    #Store query embedding and retrieve similar document chunks
    store_query_embedding(query)
    search_tool = GetDocSearchResultsTool()
    return search_tool._retrieve_similar_chunks(query)

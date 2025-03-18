from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv
import os
import uuid
from datetime import datetime

load_dotenv()

COSMOS_DB_URL = os.getenv("COSMOS_DB_URL")
COSMOS_DB_KEY = os.getenv("COSMOS_DB_KEY")
COSMOS_DB_LANGGRAPH_DATABASE = os.getenv("COSMOS_DB_LANGGRAPH_DATABASE")  
CHAT_HISTORY_CONTAINER_NAME = os.getenv("CHAT_HISTORY_CONTAINER_NAME")

client = CosmosClient(COSMOS_DB_URL, credential=COSMOS_DB_KEY)

langgraph_db = client.create_database_if_not_exists(COSMOS_DB_LANGGRAPH_DATABASE)

# chat history container inside LangGraph chatbot database
chat_history_container = langgraph_db.create_container_if_not_exists(
    id=CHAT_HISTORY_CONTAINER_NAME,
    partition_key=PartitionKey(path="/user_id")
)

def store_chat_history(user_id, user_input, bot_response):
    #Stores user chat history in Cosmos DB LangGraph chatbot database
    chat_document = {   
        "id": str(uuid.uuid4()),  # Unique ID for each chat entry
        "user_id": user_id,
        "user_input": user_input,
        "bot_response": bot_response,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    chat_history_container.upsert_item(chat_document)
    print(f"Chat history stored for user {user_id} in LangGraph Chatbot.")

def get_chat_history(user_id):    
    #Retrieves chat history from Cosmos DB
    query = f"SELECT * FROM c WHERE c.user_id = '{user_id}' ORDER BY c.timestamp DESC"
    results = list(chat_history_container.query_items(query=query, enable_cross_partition_query=True))
    
    return [(item["user_input"], item["bot_response"]) for item in results]

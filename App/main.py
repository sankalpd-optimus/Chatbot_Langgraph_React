from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import store_chat_history, get_chat_history
from graph import agent_executor, AgentState
from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv
import os

load_dotenv()

COSMOS_DB_URL = os.getenv("COSMOS_DB_URL")
COSMOS_DB_KEY = os.getenv("COSMOS_DB_KEY")
COSMOS_DB_LANGGRAPH_DATABASE = os.getenv("COSMOS_DB_LANGGRAPH_DATABASE")
CHAT_HISTORY_CONTAINER_NAME = os.getenv("CHAT_HISTORY_CONTAINER_NAME")

client = CosmosClient(COSMOS_DB_URL, credential=COSMOS_DB_KEY)
database = client.create_database_if_not_exists(COSMOS_DB_LANGGRAPH_DATABASE)

chat_history_container = database.create_container_if_not_exists(
    id=CHAT_HISTORY_CONTAINER_NAME,
    partition_key=PartitionKey(path="/user_id")
)

app = FastAPI()

# Request model for chat endpoint
class ChatRequest(BaseModel):
    user_id: str
    user_input: str

@app.post("/chat")
async def chat(request: ChatRequest):
    user_id = request.user_id
    user_input = request.user_input.strip()

    if user_input.lower() in ["show my chat history", "my chat history", "history"]:
        history = get_chat_history(user_id)
        if not history:
            return {"response": "No chat history found for this user."}
        return {"response": history}

    if not user_input:
        raise HTTPException(status_code=400, detail="User input cannot be empty.")

    try:
        # Initialize AgentState and set user query
        state = AgentState(user_query=user_input)

        # Execute agent and get the bot response
        result_state = agent_executor.invoke(state)

        
        bot_response = result_state["final_response"] or "Sorry, no response generated."
        store_chat_history(user_id, user_input, bot_response)

        return {"user_id": user_id, "response": bot_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")



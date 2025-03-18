from langgraph.graph import StateGraph, END
from langchain_openai import AzureChatOpenAI  
from langchain.schema import HumanMessage
from tools import GetDocSearchResults_Tool, WebSearchTool  
from typing import Optional
import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()
AZURE_OPENAI_MODEL_NAME = os.getenv("AZURE_OPENAI_MODEL_NAME")

llm = AzureChatOpenAI(deployment_name=AZURE_OPENAI_MODEL_NAME, temperature=0.7)   #for final node: Generate response

# Initialize Agents
doc_search_agent = GetDocSearchResults_Tool(k=5)
web_search_agent = WebSearchTool()

@dataclass
class AgentState:       #AgentState is a non subscriptable object 
    user_query: str
    doc_search_results: Optional[str] = None
    web_search_results: Optional[str] = None
    final_response: Optional[str] = None
    next: Optional[str] = None  


graph = StateGraph(AgentState)

# Node 1: Route Query
def route_query(state: AgentState):
    query = state.user_query.lower()
    
    if "document" in query or "knowledge" in query:
        return {"next": "doc_search"}  
    else:
        return {"next": "web_search"}  

# Node 2: Get Document Search Results
def get_doc_search_results(state: AgentState):
    state.doc_search_results = doc_search_agent._run(state.user_query)
    return {"doc_search_results": state.doc_search_results}
    if not state.doc_search_results:
        state.doc_search_results = "No relevant document found."

# Node 3: Get Web Search Results
def get_web_search_results(state: AgentState):
    web_search_tool = WebSearchTool()  
    state.web_search_results = web_search_tool._run(state.user_query)  
    return {"web_search_results": state.web_search_results}

# Node 4: Generate Response
def generate_response(state: AgentState):
    context = f"Document Search: {state.doc_search_results}\nWeb Search: {state.web_search_results}"
    response = llm.invoke([HumanMessage(content=context)])  
    if hasattr(response, "content"):
        final_response = response.content
    else:
        final_response = str(response)

    return {"final_response": final_response}
    next: Optional[str] = None  

# Register Nodes
graph.add_node("route_query", route_query)
graph.add_node("doc_search", get_doc_search_results)
graph.add_node("web_search", get_web_search_results)
graph.add_node("generate_response", generate_response)

#Edge Definitions
graph.add_conditional_edges(
    "route_query",
    lambda state: state.next,  
)

graph.add_edge("doc_search", "generate_response")
graph.add_edge("web_search", "generate_response")
graph.add_edge("generate_response", END)  

# Set Entry & Exit Points
graph.set_entry_point("route_query")

# Compile the Graph
agent_executor = graph.compile()

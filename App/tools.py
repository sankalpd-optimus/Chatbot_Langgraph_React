from langchain.tools import BaseTool
from pydantic import BaseModel
from typing import Type
import asyncio
from concurrent.futures import ThreadPoolExecutor
from doc_search import GetDocSearchResultsTool  
from web_search import BingSearchRetriever  

#  Schema for input arguments
class DocSearchInput(BaseModel):
    query: str

class GetDocSearchResults_Tool(BaseTool):
    name: str = "documents_retrieval"
    description: str = "Retrieves documents from knowledge base using vector similarity search."
    args_schema: Type[BaseModel] = DocSearchInput  

    k: int = 10  # Number of results to return

    def _run(self, query: str) -> str:
        retriever = GetDocSearchResultsTool(k=self.k)  

        if hasattr(retriever, "invoke"):
            results = retriever.invoke(query)
        else:
            raise AttributeError("Error: 'GetDocSearchResultsTool' has no method 'run' or 'invoke'.")

        print(f" Debug: Document search results for query '{query}': {results}")  # Debug output

        return results if results else "No relevant document found."

    async def _arun(self, query: str) -> str:
        loop = asyncio.get_event_loop()
        retriever = GetDocSearchResultsTool(k=self.k)

        # Use invoke() instead of run()
        if hasattr(retriever, "invoke"):
            results = await loop.run_in_executor(ThreadPoolExecutor(), retriever.invoke, query)
        else:
            raise AttributeError("Error: 'GetDocSearchResultsTool' has no method 'run' or 'invoke'.")

        print(f" Debug (async): Document search results for query '{query}': {results}")  # Debug output

        return results if results else "No relevant document found."



# Schema for web search input
class WebSearchInput(BaseModel):
    query: str  

class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = "Searches the web for information using Bing Search."
    args_schema: Type[BaseModel] = WebSearchInput  

    def _run(self, query: str) -> str:
        retriever = BingSearchRetriever()
        results = retriever.invoke(query)

        print(f" Debug: Web search results for query '{query}': {results}")  # Debug output

        return results if results else "No relevant web results found."

    async def _arun(self, query: str) -> str:
        retriever = BingSearchRetriever()
        
        loop = asyncio.get_running_loop()
        results = await loop.run_in_executor(ThreadPoolExecutor(), retriever.invoke, query)

        print(f" Debug (async): Web search results for query '{query}': {results}")  # Debug output

        return results if results else "No relevant web results found."


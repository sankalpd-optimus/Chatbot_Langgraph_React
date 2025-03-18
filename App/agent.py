from typing import Optional
from tools import get_document_search_results, get_web_search_results, generate_final_response
from dataclasses import dataclass  # Ensures proper instance variable handling

@dataclass
class AgentState:
    user_query: str
    doc_search_results: Optional[str] = None
    web_search_results: Optional[str] = None
    final_response: Optional[str] = None
    next: Optional[str] = None  


def agent_executor(state: AgentState) -> AgentState:

    if state.doc_search_results is None:
        state.doc_search_results = get_document_search_results(state.user_query)

    if state.web_search_results is None:
        if not state.doc_search_results or len(state.doc_search_results) < 3:  
            state.web_search_results = get_web_search_results(state.user_query)

    if state.final_response is None:
        state.final_response = generate_final_response(state)

    return state

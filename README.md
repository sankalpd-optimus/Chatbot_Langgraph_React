To run this, open terminal in your IDE  
step 1: uvicorn app.main:app --reload ( default host:_ http://localhost:8000 )
step 2: streamlit run bot.py

You can trigger a specific agent using:

@doc for document-based queries (Upload a document to use this)
@web for web search
@sql for structured data queries




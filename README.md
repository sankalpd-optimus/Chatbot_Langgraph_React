To run this, open terminal in your IDE  
step 1: uvicorn app.main:app --reload ( default host:_ http://localhost:8000 )
step 2: nmp run dev 

the chatbot has several features:
1. toggle between light/dark mode
2. clear conversation
3. view chat history

It has 2 agents Doc_search agent and Web_search agent (Bing)
To trigger doc_search use keyword based routing such as "document" and "knowledge".

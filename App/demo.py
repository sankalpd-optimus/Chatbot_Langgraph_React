from doc_search import GetDocSearchResultsTool

retriever = GetDocSearchResultsTool(k=5)
results = retriever.invoke("what are the guidelines for reporting managers")
print(results)








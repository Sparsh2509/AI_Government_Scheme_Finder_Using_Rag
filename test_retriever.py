from rag.retriever import retrieve_schemes

docs = retrieve_schemes("schemes for farmers in India")

for doc in docs:
    print(doc.metadata['scheme_name'])
    print(doc.page_content[:200])
    print("---")
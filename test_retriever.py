from rag.retriever import retrieve_schemes

docs = retrieve_schemes("schemes for farmers in India")

print(f"Total docs retrieved: {len(docs)}")

for doc in docs:
    print(doc.metadata)
    print(doc.page_content[:200])
    print("---")
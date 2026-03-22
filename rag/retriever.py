from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def retrieve_schemes(query):
    client = QdrantClient(path="./qdrant_db")
    
    vectorstore = QdrantVectorStore(
        client=client,
        collection_name="schemes",
        embedding=embeddings
    )
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(query)
    
    return docs
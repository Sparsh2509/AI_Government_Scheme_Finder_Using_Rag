import os
import re
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def clean_scheme_name(name):
    # Remove everything after "Are you sure"
    name = re.sub(r'Are you sure.*', '', name)
    # Remove Hindi text garbage
    name = re.sub(r'[^\x00-\x7F]+', '', name)
    return name.strip()

def retrieve_schemes(query):
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )
    
    vectorstore = QdrantVectorStore(
        client=client,
        collection_name="schemes",
        embedding=embeddings
    )
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(query)
    
    # Clean scheme names
    for doc in docs:
        doc.metadata['scheme_name'] = clean_scheme_name(doc.metadata['scheme_name'])
    
    return docs
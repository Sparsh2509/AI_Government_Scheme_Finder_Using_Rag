import os
import re
from functools import lru_cache
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()

hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    raise ValueError("HF_TOKEN not found in environment variables")

embeddings = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=hf_token
)

def clean_scheme_name(name):
    name = re.sub(r'Are you sure.*', '', name)
    name = re.sub(r'[^\x00-\x7F]+', '', name)
    return name.strip()

@lru_cache(maxsize=1)
def get_vectorstore():
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )
    return QdrantVectorStore(
        client=client,
        collection_name="schemes",
        embedding=embeddings
    )

def retrieve_schemes(query, state=None):
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    docs = retriever.invoke(query)

    # Filter by state if possible
    if state:
        state_docs = [doc for doc in docs if state.lower() in doc.page_content.lower()]
        if state_docs:
            docs = state_docs[:5]
        else:
            docs = docs[:5]

    for doc in docs:
        doc.metadata['scheme_name'] = clean_scheme_name(doc.metadata['scheme_name'])

    return docs
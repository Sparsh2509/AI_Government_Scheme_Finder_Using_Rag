from huggingface_hub import hf_hub_download, list_repo_files
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import fitz  # pymupdf
import os
import tempfile
import time
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

load_dotenv()

#  SETTINGS 
BATCH_SIZE = 200
MAX_RETRIES = 3
MAX_WORKERS = 5
COLLECTION_NAME = "schemes"

#  EMBEDDINGS 
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

#  TEXT SPLITTER 
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

#  QDRANT CLIENT 
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
    timeout=300
)

# Create collection if not exists
if not client.collection_exists(COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )

vectorstore = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION_NAME,
    embedding=embeddings
)

#  PDF TEXT EXTRACTION 
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()

#  BATCH UPLOAD FUNCTION 
def upload_batch(batch, batch_id):
    for attempt in range(MAX_RETRIES):
        try:
            vectorstore.add_documents(batch)
            print(f" Batch {batch_id} uploaded ({len(batch)} docs)")
            return
        except Exception as e:
            print(f" Retry {attempt+1} for batch {batch_id}...", e)
            time.sleep(5)

#  MAIN FUNCTION 
def build_vectorstore(limit=2153):
    print("Fetching PDF list from HuggingFace...")

    files = list(list_repo_files("shrijayan/gov_myscheme", repo_type="dataset"))
    pdf_files = [f for f in files if f.endswith('.pdf') and 'copy' not in f]
    pdf_files = pdf_files[:limit]

    print(f"Total PDFs to process: {len(pdf_files)}")

    batch_counter = 0

    for i, pdf_file in enumerate(pdf_files):
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                path = hf_hub_download(
                    repo_id="shrijayan/gov_myscheme",
                    filename=pdf_file,
                    repo_type="dataset",
                    local_dir=tmpdir
                )

                text = extract_text_from_pdf(path)

                if not text:
                    print(f"[{i+1}] Empty PDF skipped: {pdf_file}")
                    continue

                lines = [l.strip() for l in text.split('\n') if l.strip()]
                scheme_name = lines[0] if lines else os.path.basename(pdf_file)

                doc = Document(
                    page_content=text,
                    metadata={
                        "scheme_name": scheme_name,
                        "source": pdf_file
                    }
                )

                chunks = splitter.split_documents([doc])

                print(f"[{i+1}/{len(pdf_files)}] {scheme_name} → {len(chunks)} chunks")

                # Upload in batches using threads
                batches = [
                    chunks[j:j+BATCH_SIZE]
                    for j in range(0, len(chunks), BATCH_SIZE)
                ]

                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    for batch in batches:
                        executor.submit(upload_batch, batch, batch_counter)
                        batch_counter += 1

        except Exception as e:
            print(f"[{i+1}] Failed: {pdf_file} — {e}")
            continue

    print("\n Vectorstore built successfully!")


if __name__ == "__main__":
    build_vectorstore(limit=2153)
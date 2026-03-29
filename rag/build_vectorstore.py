from huggingface_hub import hf_hub_download, list_repo_files
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import fitz  # pymupdf
import os
import tempfile
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Text splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file"""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()

def build_vectorstore(limit=2153):
    """Download PDFs, extract text, embed and store in Qdrant"""
    
    print("Fetching PDF list from HuggingFace...")
    files = list(list_repo_files("shrijayan/gov_myscheme", repo_type="dataset"))
    pdf_files = [f for f in files if f.endswith('.pdf') and 'copy' not in f]
    pdf_files = pdf_files[:limit]
    
    print(f"Total PDFs to process: {len(pdf_files)}")

    all_docs = []

    for i, pdf_file in enumerate(pdf_files):
        try:
            # Download to temp file
            with tempfile.TemporaryDirectory() as tmpdir:
                path = hf_hub_download(
                    repo_id="shrijayan/gov_myscheme",
                    filename=pdf_file,
                    repo_type="dataset",
                    local_dir=tmpdir
                )

                # Extract text
                text = extract_text_from_pdf(path)

                if not text:
                    print(f"[{i+1}] Empty PDF skipped: {pdf_file}")
                    continue

                # Get scheme name from filename
                lines = [l.strip() for l in text.split('\n') if l.strip()]
                scheme_name = lines[0] if lines else os.path.basename(pdf_file)

                # Create document
                doc = Document(
                    page_content=text,
                    metadata={
                        "scheme_name": scheme_name,
                        "source": pdf_file
                    }
                )

                # Chunk it
                chunks = splitter.split_documents([doc])
                all_docs.extend(chunks)

                print(f"[{i+1}/{len(pdf_files)}] Processed: {scheme_name} — {len(chunks)} chunks")

        except Exception as e:
            print(f"[{i+1}] Failed: {pdf_file} — {e}")
            continue

    print(f"\nTotal chunks created: {len(all_docs)}")
    print("Storing in Qdrant...")

    # Store in Qdrant (local)
    # correct


    client = QdrantClient(path="./qdrant_db")

    # Create collection manually
    client.recreate_collection(
        collection_name="schemes",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )

    vectorstore = QdrantVectorStore(
        client=client,
        collection_name="schemes",
        embedding=embeddings
    )

    # Add documents
    vectorstore.add_documents(all_docs)
    print("Vectorstore built successfully!")

if __name__ == "__main__":
    build_vectorstore(limit=500)
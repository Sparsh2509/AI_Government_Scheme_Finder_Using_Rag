from huggingface_hub import hf_hub_download, list_repo_files
import os

# List all files in the dataset
files = list(list_repo_files("shrijayan/gov_myscheme", repo_type="dataset"))

# Filter only PDFs
pdf_files = [f for f in files if f.endswith('.pdf') and 'copy' not in f]

print(f"Total PDFs: {len(pdf_files)}")
print(pdf_files[:5])  
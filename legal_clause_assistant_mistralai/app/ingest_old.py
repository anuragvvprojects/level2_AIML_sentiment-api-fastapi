import json
import os
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from tqdm import tqdm

CUAD_FILE = "data/raw/CUADv1.json"
VECTOR_DB_DIR = "vector_store/chroma.db"

def load_cuad_documents(path):
    with open(path, "r") as f:
        data = json.load(f)

    documents = []
    for doc in data:
        doc_name = doc.get("doc_name", "unknown_doc")
        full_text = doc["full_text"]
        labels = doc.get("labels", {})

        # Build metadata from labels (clause types present)
        clause_types = [k for k, v in labels.items() if v]
        metadata = {
            "doc_name": doc_name,
            "clause_types": clause_types,
        }

        documents.append(Document(page_content=full_text, metadata=metadata))
    return documents

def chunk_documents(docs, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return splitter.split_documents(docs)

def embed_and_store(chunks):
    embedder = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
    db = Chroma.from_documents(chunks, embedding=embedder, persist_directory=VECTOR_DB_DIR)
    db.persist()
    print(f"✅ Stored {len(chunks)} chunks in vector DB at: {VECTOR_DB_DIR}")

def main():
    print("📥 Loading CUAD documents...")
    docs = load_cuad_documents(CUAD_FILE)
    print(f"Loaded {len(docs)} contracts.")

    print("✂️ Chunking documents...")
    chunks = chunk_documents(docs)
    print(f"Generated {len(chunks)} chunks.")

    print("🔗 Embedding and storing in vector DB...")
    embed_and_store(chunks)

if __name__ == "__main__":
    main()

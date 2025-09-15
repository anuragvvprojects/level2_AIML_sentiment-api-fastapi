import os
import pandas as pd
import unicodedata
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from difflib import get_close_matches

CSV_PATH = "data/raw/CUAD_v1/master_clauses.csv"
TXT_DIR = "data/raw/CUAD_v1/full_contract_txt/"
VECTOR_DB_DIR = "vector_store"

def normalize_filename(name):
    name = name.replace(".pdf", "").replace(".PDF", "")
    name = name.replace("&", "_").replace("'", "").replace("’", "")
    name = name.replace("A&R", "A_R").replace(" - ", "-").strip()
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("utf-8")
    return name

def get_best_match(filename, txt_files):
    matches = get_close_matches(filename + ".txt", txt_files, n=1, cutoff=0.85)
    return matches[0] if matches else None

def load_documents():
    df = pd.read_csv(CSV_PATH)
    txt_files = os.listdir(TXT_DIR)
    txt_set = set(txt_files)
    documents = []
    unmatched_files = []

    for _, row in df.iterrows():
        raw_fname = row["Filename"]
        norm_fname = normalize_filename(raw_fname)
        txt_file = f"{norm_fname}.txt"

        if txt_file not in txt_set:
            alt = get_best_match(norm_fname, txt_files)
            if alt:
                txt_file = alt
            else:
                unmatched_files.append(txt_file)
                continue

        txt_path = os.path.join(TXT_DIR, txt_file)

        try:
            with open(txt_path, encoding="utf8", errors="ignore") as f:
                full_text = f.read()
        except Exception as e:
            print(f"⚠️ Error reading {txt_path}: {e}")
            continue

        clause_types = [col for col in df.columns[1:] if pd.notnull(row[col])]
        metadata = {
            "doc_name": txt_file.replace(".txt", ""),
            "clause_types": ", ".join(clause_types),  # converted to string
        }

        documents.append(Document(page_content=full_text, metadata=metadata))

    if unmatched_files:
        print(f"⚠️ {len(unmatched_files)} contracts could not be matched to TXT files.")
        print("Sample unmatched:", unmatched_files[:5])

    return documents

def chunk_documents(docs, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(docs)

def embed_and_store(chunks):
    embedder = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
    db = Chroma.from_documents(chunks, embedding=embedder, persist_directory=VECTOR_DB_DIR)
    db.persist()
    print(f"✅ Stored {len(chunks)} chunks in vector DB at: {VECTOR_DB_DIR}")

def main():
    print("📥 Loading documents with smart matching...")
    docs = load_documents()
    print(f"Loaded {len(docs)} contracts into memory.")

    print("✂️ Chunking documents...")
    chunks = chunk_documents(docs)
    print(f"Generated {len(chunks)} chunks.")

    print("🔗 Embedding and storing in vector DB...")
    embed_and_store(chunks)

if __name__ == "__main__":
    main()

# 🧠 Legal Clause Assistant (Local RAG with Meta-Llama-Guard-2-8B)

This project builds a legal clause retrieval-augmented generation (RAG) pipeline to answer contract-related questions using the [CUAD dataset](https://huggingface.co/datasets/TheAtticusProject/cuad) and a local **Meta-Llama-Guard-2-8B** model.

---

## 📁 Project Structure

```
legal_clause_assistant_llama3/
├── app/
│   ├── ingest.py                  # Ingests and embeds documents into Chroma DB
│   ├── qa_chain_llama.py         # LLaMA-based RAG chain logic
│   ├── test_qa_chain_llama.py    # Script to test the RAG pipeline
│   └── test_llama_guard.py       # Standalone model test
├── data/
│   └── raw/
│       └── CUAD_v1/              # CUAD dataset (CSV + TXT + metadata)
├── vector_store/                 # Persisted Chroma DB
├── llamaenv/                     # Python virtual environment
└── README.md
```

---

## ⚙️ Setup

### 1. Clone and create virtualenv

```bash
git clone <repo> legal_clause_assistant_llama3
cd legal_clause_assistant_llama3
python3 -m venv llamaenv
source llamaenv/bin/activate
```

### 2. Install dependencies

```bash
pip install torch transformers accelerate bitsandbytes
pip install sentence-transformers chromadb
pip install langchain langchain-community
```

---

## 🧩 CUAD Dataset

- Download CUAD from [Zenodo](https://zenodo.org/record/4595762)
- Unzip into: `data/raw/CUAD_v1/`

We verified document–metadata alignment using:

```bash
python data/raw/CUAD_v1/test_cuad_v1_data.py
```

---

## 📥 Ingest the Corpus

```bash
python app/ingest.py
```

- 510 documents loaded
- ~73,000 chunks generated and embedded
- Stored into `vector_store/chroma.db`

---

## 🧪 Test LLaMA Model

Ensure Hugging Face login:
```bash
huggingface-cli login
```

Then test the model:
```bash
python app/test_llama_guard.py
```

---

## 🔍 Run RAG Pipeline Locally

```bash
python app/test_qa_chain_llama.py
```

- Retrieves top-5 chunks
- Feeds to Meta-Llama-Guard-2-8B
- Returns answer + metadata

---

## 🔁 Notes

- We used `transformers` + `bitsandbytes` for 8-bit quantized model loading.
- Metadata mismatch during ingestion was handled via filtering.
- Hugging Face gated repo access was configured via CLI login.

---

## 🔮 Next Steps

- Build Gradio UI (`gradio_ui_llama.py`)
- Add FastAPI endpoint (`main_llama.py`)
- Add eval pipeline (`eval_llama.py`)

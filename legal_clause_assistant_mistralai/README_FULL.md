# 🧠 Legal Clause Assistant (Local RAG using Meta-Llama-Guard-2-8B)

This is a complete Retrieval-Augmented Generation (RAG) project to assist with legal clause understanding, powered by **Meta-Llama-Guard-2-8B** running locally using `transformers` + `bitsandbytes`.

It uses the CUAD dataset to retrieve relevant legal contract segments and generate contextual answers.

---

## 📂 Project Structure

```
legal_clause_assistant_llama3/
├── app/
│   ├── ingest.py                  # Load, chunk, and embed CUAD documents into Chroma DB
│   ├── retriever.py               # Handles retrieval from the vector store
│   ├── prompts.py                 # Prompt templates for the LLM
│   ├── qa_chain_llama.py          # RAG chain using local Meta-Llama model
│   ├── test_qa_chain_llama.py     # Test script for full RAG pipeline
│   ├── test_llama_guard.py        # Standalone model loading and response test
│   ├── main_llama.py              # FastAPI backend (planned)
│   └── gradio_ui_llama.py         # Gradio UI interface (planned)
│
├── data/
│   └── raw/
│       └── CUAD_v1/
│           ├── master_clauses.csv
│           ├── *.txt                         # 498 contract documents
│           ├── test_cuad_v1_data.py          # Test doc-CSV consistency
│           ├── diagnose_missing_txt.py       # Analyze missing file mappings
│           └── analyze_data.py               # Understand JSON structure
│
├── eval/
│   ├── eval_pipeline.py           # Accuracy and coverage scoring (planned)
│   └── eval_data.csv              # Placeholder for manual Q&A evaluation
│
├── vector_store/
│   └── chroma.db/                 # Persisted vector DB for fast retrieval
│
├── llamaenv/                      # Python virtual environment
├── README.md
└── requirements.txt (planned)
```

---

## ✅ Progress Summary

### 🔸 Dataset Setup
- Downloaded CUAD dataset from Zenodo
- Verified 498 out of 510 documents had corresponding `.txt` files
- Diagnosed and fixed file name mismatches

### 🔸 Vector Store Creation
- Loaded documents via `ingest.py`
- Chunked into 73,706 segments using LangChain
- Used `sentence-transformers` (BAAI/bge-base-en-v1.5) for embeddings
- Stored into `Chroma` vector DB

### 🔸 RAG Pipeline (LLaMA version)
- Created `qa_chain_llama.py` with `RetrievalQA` from LangChain
- Tested local responses using `test_qa_chain_llama.py`

### 🔸 Model Testing
- Got approved for Hugging Face gated model: `meta-llama/Meta-Llama-Guard-2-8B`
- Logged in via `huggingface-cli login`
- Loaded the model using `transformers` with `bitsandbytes` (8-bit quantization)
- Verified token access and download via `test_llama_guard.py`

### 🔸 Issues Handled
- Filtered malformed JSON structure in earlier CUAD JSON file
- Converted to using CSV+TXT from CUAD v1 instead
- Addressed Chroma metadata errors by sanitizing field types
- Avoided re-ingestion by reusing same embeddings across variants

---

## 💻 Setup Instructions

### 🔧 1. Create and activate environment
```bash
python3 -m venv llamaenv
source llamaenv/bin/activate
```

### 📦 2. Install dependencies
```bash
pip install torch transformers accelerate bitsandbytes
pip install sentence-transformers chromadb
pip install langchain langchain-community
```

### 🗂 3. Prepare CUAD data
- Download CUAD v1 ZIP from: https://zenodo.org/record/4595762
- Unzip to: `data/raw/CUAD_v1/`

---

## 🚀 Running the Project

### 📥 Embed Documents
```bash
python app/ingest.py
```

### 🧠 Test LLaMA Model Standalone
```bash
python app/test_llama_guard.py
```

### 🔍 Test RAG Pipeline
```bash
python app/test_qa_chain_llama.py
```

---

## 🔮 Upcoming Work

- ✅ Restore modular `retriever.py` and `prompts.py`
- 🔄 Add `main_llama.py` FastAPI backend
- 💬 Add `gradio_ui_llama.py` for interactive UI
- 📊 Add `eval_pipeline.py` for clause matching evaluation
- 📦 Add `requirements.txt` for reproducibility

---

## 🙌 Contributions & Extensions

This scaffold can be extended for:
- Clause classification or summarization
- Fine-tuning on downstream legal tasks
- Model comparison (OpenAI vs LLaMA vs Mistral)
- UI deployment (Streamlit, Gradio, web frontend)


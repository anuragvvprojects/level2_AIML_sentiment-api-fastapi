# 🧠 Legal Clause Assistant (Local RAG using Meta-Llama-Guard-2-8B)

This is a complete Retrieval-Augmented Generation (RAG) project to assist with legal clause understanding, powered by **Meta-Llama-Guard-2-8B** running locally using `transformers` + `bitsandbytes`.

It uses the CUAD dataset to retrieve relevant legal contract segments and generate contextual answers.

---

## 📂 Project Structure

```
legal_clause_assistant/
├── app/
│   ├── ingest.py                   # Chunk + embed CUAD into Chroma
│   ├── retriever.py                # Load vector store & retrieve
│   ├── qa_chain.py                 # QA pipeline using OpenAI
│   ├── qa_chain_mistral.py         # ✅ QA pipeline using Mistral-7B
│   ├── prompts.py                  # Prompt templates
│   ├── test_qa_chain_openai.py     # Test with OpenAI chain
│   ├── test_qa_chain_mistral.py    # ✅ Test with Mistral chain
│   ├── test_mistralai.py           # Standalone generation test
│   ├── eval.py                     # Evaluation placeholder
│   └── utils.py                    # Helpers for chunking, cleaning
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
├── vectorstore/                   # Chroma DB directory
├── llmragenv/                     # Python venv (exclude in Git)
├── README.md
├── progress.md                    # 📈 Task and milestone log
└── requirements.txt

```
------------------------------------------
## 📌 What Each Part Does
### ✅ Ingestion
ingest.py:
- Loads CUAD contracts (text + clause metadata)
- hunks them
- Embeds chunks with bge-base-en-v1.5
- Saves them in Chroma vector store

### ✅ RAG Pipeline
retriever.py:
- Loads Chroma DB
- Uses embedding model to find relevant chunks
- qa_chain.py / qa_chain_mistral.py:
- Constructs LangChain RetrievalQA with:

Retriever
- LLM (OpenAI or Mistral)
- Prompt from prompts.py
- prompts.py:
- Stores prompt templates (question answering, summarization, etc.)

### ✅ Test Harness
test_qa_chain_openai.py: test OpenAI QA
test_qa_chain_mistral.py: 🔁 test QA with Mistral
test_mistralai.py: raw Mistral output (already tested ✅)

### 🔄 Evaluation (Placeholder)
eval.py: placeholder to measure:
- Precision/Recall/F1 if clause detection is supervised
- Human-in-the-loop validation for QA correctness
---
------------------------------------------
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
------------------------------------------
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

------------------------------------------

## 🚀 Quickstart

### 1. 📦 Install

```bash
python3 -m venv llmragenv
source llmragenv/bin/activate

pip install -r requirements.txt
```

> Ensure you have CUDA + bitsandbytes dependencies installed for GPU support.

---

### 2. 📄 Prepare Data

- Download CUAD v1 from [Zenodo](https://zenodo.org/record/4592955) or GitHub.
- Place `master_clauses.csv` and `.txt` files into `data/raw/CUAD_v1/`.

---

### 3. 🔌 Ingest Documents

```bash
python app/ingest.py
```

- This will:
  - Load and chunk contracts
  - Embed them
  - Store in `Chroma` vector DB

---

### 4. 🧪 Test the Model

#### ✅ Test local Mistral model:

```bash
python app/test_mistralai.py
```

#### ✅ Test full QA chain (retriever + Mistral):

```bash
python app/test_qa_chain_mistral.py
```

------------------------------------------

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


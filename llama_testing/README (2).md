# 🧠 Legal Clause Assistant (RAG with CUAD + Mistral-7B)

This project builds a local **RAG-based legal question-answering assistant** using the [CUAD dataset](https://github.com/TheAtticusProject/cuad) and the `Mistral-7B-Instruct-v0.1` model (quantized). It allows answering questions about real-world contract clauses using embedded knowledge.

---

## 🔧 Features

- ✅ **CUAD document chunking & vector indexing**
- 🔎 **Chroma** vector store with `bge-base-en-v1.5` embeddings
- 🤖 **LLM-powered QA pipeline**
  - `OpenAI GPT-4` (optional)
  - ✅ `Mistral-7B-Instruct-v0.1` (local with 4-bit quantization)
- 🧩 Prompt templates for customizable instruction formatting
- 🖼️ Modular code structure for API/UI/eval additions

---

## 🗂️ Project Structure

```
legal_clause_assistant_llama3/
│
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
│
├── data/
│   ├── raw/                        # CUAD files (.csv, .txt)
│   └── processed/                  # Cleaned or normalized content
│
├── vectorstore/                   # Chroma DB directory
├── llmragenv/                     # Python venv (exclude in Git)
├── README.md
├── progress.md                    # 📈 Task and milestone log
└── requirements.txt
```

---

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

---

## 🧠 Progress Summary

See [`progress.md`](./progress.md) for a full timeline.

Highlights:
- CUAD dataset diagnosed and cleaned
- 73,706 contract chunks embedded with BAAI/bge-base-en-v1.5
- GPT-4 QA chain validated
- 🌀 Switched to local Mistral for full offline capability
- Vector store + Retriever + Prompt templating integrated

---

## 🛠️ Next Steps

- [ ] FastAPI or Gradio UI
- [ ] Evaluation harness (human or heuristic)
- [ ] Prompt tuning and clause-type classification
- [ ] Deployment + Dockerization

---

## 📚 References

- CUAD Dataset: https://github.com/TheAtticusProject/cuad
- Mistral: https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1
- LangChain: https://python.langchain.com

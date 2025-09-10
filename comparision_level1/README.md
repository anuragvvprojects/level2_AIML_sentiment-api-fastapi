`# 🧠 	

## Level 1 Implementation
This repository demonstrates how to build and deploy a minimal machine learning API using both **FastAPI** and **Gradio** interfaces. It uses a pretrained Hugging Face sentiment analysis model and serves it through two deployment-friendly methods.

---

## 🚀 Features

- ✅ Sentiment analysis using `distilbert-base-uncased-finetuned-sst-2-english`
- ✅ REST API with FastAPI (`POST /predict`)
- ✅ No-code UI using Gradio
- ✅ Lightweight, deployment-ready setup
- ✅ Follows production-style environment isolation

---

## 📁 Project Structure

```
ml_deploy_demo/
│
├── app_fastapi.py     # FastAPI-based API server
├── app_gradio.py      # Gradio-based GUI interface
├── requirements.txt   # All Python dependencies
└── README.md          # Project documentation
```
---

## 📦 Requirements

Contents of `requirements.txt`:

```
transformers==4.41.2
torch==2.3.0
fastapi==0.111.0
uvicorn==0.30.1
gradio==4.32.1
pydantic==2.7.1
```

---
## 🔧 Installation

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd ml_deploy_demo
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate       # On Linux/macOS
# OR
venv\Scripts\activate          # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🧪 Demo 1: FastAPI (API Interface)

### ▶️ Run Server

```bash
uvicorn app_fastapi:app --reload
```

### 🌐 API Docs

Visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
Use Swagger UI to test the `/predict` endpoint.

### 🔁 Example cURL Request

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this app!"}'
```

---

## 🧪 Demo 2: Gradio (No-Code UI)

### ▶️ Run Gradio App

```bash
python app_gradio.py
```

The app launches in your browser at [http://127.0.0.1:7860](http://127.0.0.1:7860)

---

## 🧠 Learnings So Far

- Understood **ML model deployment pipelines**
- Built APIs and UIs for real models
- Learned the role of APIs in **production ML workflows**
- Practiced environment setup, inference serving, and interface building

---

## 🛣️ Next Steps

- [ ] Add preprocessing (text cleaning, batching)
- [ ] Train and swap in a custom model
- [ ] Add Docker support for true production-readiness
- [ ] Deploy to Hugging Face Spaces or Render

---

## 👨‍💻 Author

Built by Anurag V.V. as part of a 3-day AI/ML sprint to go from zero to deploy-ready ML engineer.

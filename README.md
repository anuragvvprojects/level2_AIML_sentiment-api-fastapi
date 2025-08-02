# Level 2 Implementation
level2_implementation/
├── app/
│   └── main.py           ← FastAPI app with logging
├── model/
│   └── load_model.py     ← Model loader (singleton)
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md

docker build -t sentiment-api .
docker run -p 8000:8000 sentiment-api

### Testing 
### ✅ Send a Request (Terminal)
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!"}'
```
### OR

### ✅ Use Swagger UI

Open browser at [http://localhost:8000/docs](http://localhost:8000/docs)  
Try the `/predict` endpoint with sample input.




# 🧠 Sentiment Analysis API (FastAPI + Docker + Transformers)

This project demonstrates how to build, containerize, and serve a machine learning model using **FastAPI**, **Hugging Face Transformers**, and **Docker**, with clean logging and deployment structure. It exposes an HTTP REST API for sentiment classification of text input using a pre-trained BERT model.

---

## 🚀 Features

- ✅ FastAPI-powered RESTful API
- ✅ Hugging Face Transformers (`distilbert-base-uncased-finetuned-sst-2-english`)
- ✅ Dockerized, portable deployment
- ✅ Structured logging using custom log config
- ✅ Swagger UI for easy interaction (`/docs`)
- ✅ Ready for cloud deployment (e.g., Render, Railway)

---

## 📁 Project Structure

```
ml_deploy_demo/
├── app/
│   ├── main.py            # FastAPI app with endpoints and logging
│   ├── log_config.yaml    # Custom logging config for Uvicorn
├── model/
│   └── load_model.py      # Model loader (Hugging Face sentiment pipeline)
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker container setup
├── .dockerignore          # Ignore cache/files during build
└── README.md              # Project documentation
```

---

## 🧠 How It Works

### 🔹 Backend API: `FastAPI`

- **`POST /predict`** — Takes raw text and returns the sentiment label and score
- **`GET /`** — Health/status check
- Automatically exposes docs at `/docs` via Swagger UI

### 🔹 Model: `transformers.pipeline`

- Uses Hugging Face pipeline abstraction
- Model: `distilbert-base-uncased-finetuned-sst-2-english`
- Text is tokenized, embedded, and classified into:
  - `POSITIVE`
  - `NEGATIVE`
- Scores are softmax probabilities

### 🔹 Logging

- Controlled via `log_config.yaml`
- Prints:
  - Incoming text
  - Model prediction result
- Can be extended to log to file, external services, etc.

### 🔹 Frontend (Swagger UI)

- Navigate to `/docs` for built-in UI to test API
- Includes text input, auto-formatted request/response
- Powered by FastAPI’s OpenAPI integration

---

## 🔄 Data Flow: From User Input to Model Response

### Example Input:
```json
POST /predict
{
  "text": "This movie is amazing!"
}
```

### 🧱 Internal Execution Chain:
```
📥 User submits JSON text
 → FastAPI receives it at /predict
 → Input validated via Pydantic BaseModel
 → Sent to classifier (Hugging Face pipeline)
 → Model: DistilBERT classifies sentiment
 → Output: {'label': 'POSITIVE', 'score': 0.9998}
 → Formatted response JSON
 → Returned via Uvicorn to client
```

### 🧠 Execution Context Overview

| Component | Location | Runs Inside |
|----------|----------|-------------|
| Swagger UI | `/docs` | Browser |
| FastAPI App | `main.py` | Docker container |
| Model | `load_model.py` | Docker container |
| HTTP Server | Uvicorn | Docker container |
| Logs | Console | Docker (via `docker logs`) |


User Input (UI / curl)
    ↓
FastAPI Endpoint (/predict) [app/main.py]
    ↓
Input validation (Pydantic)
    ↓
Model Inference (transformers.pipeline) [model/load_model.py]
    ↓
Formatted Response
    ↓
FastAPI Response Layer → JSON
    ↓
Swagger UI / curl / API client


## 🧱 Detailed Component-Level Flow
| Step                      | Data                                          | Where It Happens                             | Description                                                                |
| ------------------------- | --------------------------------------------- | -------------------------------------------- | -------------------------------------------------------------------------- |
| **1. User Input**         | `"This movie is amazing!"`                    | Browser → Swagger UI (`/docs`) or API Client | User sends a POST request to `/predict`                                    |
| **2. FastAPI Endpoint**   | `InputText(text=str)`                         | `app/main.py`, FastAPI routes                | The text is parsed and validated by the Pydantic model                     |
| **3. Logging (optional)** | Logs the received text                        | `logging.info(...)` in `main.py`             | Input string is logged to console inside the Docker container              |
| **4. Model Inference**    | `transformers.pipeline("sentiment-analysis")` | `model/load_model.py` (singleton pattern)    | The model tokenizes input, forwards it through DistilBERT, then classifies |
| **5. Prediction Output**  | `{'label': 'POSITIVE', 'score': 0.9998}`      | Inside Python in memory                      | Output from Hugging Face model                                             |
| **6. Logging Output**     | Logs the result                               | Console logs (via Docker container)          | You see: `Prediction result: {'label': 'POSITIVE', 'score': ...}`          |
| **7. JSON Response**      | `{ "label": "POSITIVE", "score": 0.9998 }`    | `FastAPI → Uvicorn → HTTP Response`          | The output is serialized into JSON                                         |
| **8. Client/UI Output**   | Same JSON                                     | Swagger UI / curl response window            | User sees prediction result                                                |

## 🧭 What Runs Where (Execution Context)

| Component               | File                              | Runs Inside                                   |
| ----------------------- | --------------------------------- | --------------------------------------------- |
| **UI (Swagger)**        | Auto-generated by FastAPI         | Browser                                       |
| **API Server**          | `main.py` (FastAPI)               | Docker container                              |
| **Model**               | `load_model.py` → `pipeline(...)` | Docker container (in memory after first load) |
| **Logging**             | Console output                    | Docker container (`docker logs`)              |
| **Uvicorn ASGI Server** | Via Docker CMD                    | Docker container (acts as HTTP server)        |


---

## 🎯 Example Usage

### ✅ Send a Request (Terminal)

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!"}'
```

Response:
```json
{
  "label": "POSITIVE",
  "score": 0.9998
}
```

### ✅ Use Swagger UI

Open browser at [http://localhost:8000/docs](http://localhost:8000/docs)  
Try the `/predict` endpoint with sample input.

---

## 🐳 Dockerized Deployment

### Build the Docker image

```bash
docker build -t sentiment-api .
```

### Run the container

```bash
docker run -p 8000:8000 sentiment-api
```

### Stop a running container

```bash
docker ps        # get container ID
docker stop <container_id>
```

---

## 🔧 `Dockerfile` Explanation

```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "app/log_config.yaml"]
```

- Uses `python:3.10` base image
- Installs FastAPI, Transformers, Torch, etc.
- Copies app code and config
- Runs Uvicorn with custom logging config

---

## 🧾 `log_config.yaml`

```yaml
version: 1
formatters:
  default:
    format: "%(asctime)s | %(levelname)s | %(message)s"
handlers:
  console:
    class: logging.StreamHandler
    formatter: default
    level: INFO
root:
  level: INFO
  handlers: [console]
```

Controls Uvicorn log formatting and behavior.

---

## 🛠 Requirements

```
fastapi==0.111.0
uvicorn==0.30.1
transformers==4.41.2
torch==2.3.0
pydantic==2.7.1
```

Install locally with:

```bash
pip install -r requirements.txt
```

---

## 🧪 Testing the API

- `curl` for command line
- `/docs` for web UI
- Monitor logs using:

```bash
docker logs <container_id>
```

---

## 📦 To Do / Extensions

- [ ] Add `/health` and `/version` endpoints
- [ ] Add `/predict_batch` for bulk inference
- [ ] Log to file or external logging platform
- [ ] Push to GitHub and deploy to Render.com
- [ ] Add unit tests and GitHub Actions CI

---

## 👨‍💻 Author

Built by Anurag V. V. as part of a 3-day AI/ML deployment sprint.  
Goal: Achieve production-grade ML API development using modern Python, Docker, and API engineering best practices.

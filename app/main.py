from fastapi import FastAPI, HTTPException
from fastapi import Depends
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field
from typing import List, Optional

from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, generate_latest, Counter, Gauge

from . import config as cfg
from .telemetry import configure_logging
from .dependencies import get_state

log = configure_logging(cfg.LOG_LEVEL)

# Prometheus metrics
REGISTRY = CollectorRegistry()
REQUESTS = Counter("app_requests_total", "Total HTTP requests", ["method", "endpoint"], registry=REGISTRY)
READY_G = Gauge("app_ready", "Readiness gauge", registry=REGISTRY)

# FastAPI app
app = FastAPI(title="Sentiment Analysis API", version=cfg.SERVICE_VERSION)

# ----- Inference service (kept local for simplicity) -----
class SentimentService:
    def __init__(self, model_name: str, max_tokens: int, device: str = "cpu"):
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.device = device
        self._pipe = None

    def load(self):
        try:
            from transformers import pipeline  # lazy import
        except Exception as e:
            raise RuntimeError(f"Transformers not available: {e}")
        self._pipe = pipeline(
            task="sentiment-analysis",
            model=self.model_name,
            tokenizer=self.model_name,
            truncation=True,
            max_length=self.max_tokens,
            device=-1 if self.device == "cpu" else 0,
        )

    @property
    def ready(self) -> bool:
        return self._pipe is not None

    def predict(self, text: str):
        if not self._pipe:
            raise RuntimeError("Pipeline not loaded")
        res = self._pipe(text, truncation=True, max_length=self.max_tokens)[0]
        # Normalize label names
        label = str(res.get("label", "")).upper()
        score = float(res.get("score", 0.0))
        return label, score


# Attach service to state
app.state.service = SentimentService(cfg.MODEL_NAME, cfg.MAX_TOKENS, cfg.DEVICE)

# ----- Schemas -----
class PredictRequest(BaseModel):
    text: str = Field(..., description="Input text for sentiment classification")
    request_id: Optional[str] = Field(default=None)

class PredictResponse(BaseModel):
    label: str
    score: float
    model: str
    request_id: Optional[str] = None

class BatchPredictRequest(BaseModel):
    texts: List[str]

class BatchPredictResponseItem(BaseModel):
    label: str
    score: float

class BatchPredictResponse(BaseModel):
    items: List[BatchPredictResponseItem]
    count: int
    model: str

# ----- Startup & middleware -----
@app.on_event("startup")
def on_startup():
    log.info("startup", env=cfg.APP_ENV, model=cfg.MODEL_NAME)
    try:
        app.state.service.load()
        READY_G.set(1)
        log.info("model_loaded", model=cfg.MODEL_NAME, max_tokens=cfg.MAX_TOKENS)
    except Exception as e:
        READY_G.set(0)
        log.error("model_load_failed", error=str(e))
        # Don't crash the process; let readiness indicate failure

@app.middleware("http")
async def metrics_middleware(request, call_next):
    response = await call_next(request)
    try:
        REQUESTS.labels(method=request.method, endpoint=request.url.path).inc()
    except Exception:
        pass
    return response

# ----- System endpoints -----
@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}

@app.get("/ready", tags=["system"])
def ready():
    return {"ready": bool(app.state.service and app.state.service.ready)}

@app.get("/version", tags=["system"])
def version():
    return {
        "service_version": app.version,
        "model_name": cfg.MODEL_NAME,
        "max_tokens": cfg.MAX_TOKENS,
    }

@app.get("/metrics")
def metrics():
    data = generate_latest(REGISTRY)
    return PlainTextResponse(data.decode("utf-8"), media_type=CONTENT_TYPE_LATEST)

# ----- Prediction endpoints -----
@app.post("/predict", response_model=PredictResponse, tags=["inference"])
def predict(payload: PredictRequest):
    if not app.state.service.ready:
        raise HTTPException(status_code=503, detail="Model not loaded")
    label, score = app.state.service.predict(payload.text)
    return PredictResponse(label=label, score=score, model=cfg.MODEL_NAME, request_id=payload.request_id)

@app.post("/predict/batch", response_model=BatchPredictResponse, tags=["inference"])
def predict_batch(payload: BatchPredictRequest):
    if not app.state.service.ready:
        raise HTTPException(status_code=503, detail="Model not loaded")
    items = []
    for t in payload.texts:
        l, s = app.state.service.predict(t)
        items.append(BatchPredictResponseItem(label=l, score=s))
    return BatchPredictResponse(items=items, count=len(items), model=cfg.MODEL_NAME)

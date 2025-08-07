from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from app.dependencies import get_state
from app.models.schemas import BatchPredictRequest, BatchPredictResponse, BatchPredictResponseItem
from app.services.limiter import rate_limiter

router = APIRouter()

@router.post("/predict/batch", response_model=BatchPredictResponse, tags=["inference"])
def predict_batch(payload: BatchPredictRequest, request: Request, _rl = Depends(rate_limiter())):
    services = get_state(request)
    svc = getattr(services, "service", None) or getattr(services, "model_service", None)
    if not svc or not getattr(svc, "ready", False):
        raise HTTPException(status_code=503, detail="Model not loaded")
    items: List[BatchPredictResponseItem] = []
    for t in payload.texts:
        l, s = svc.predict(t)
        items.append(BatchPredictResponseItem(label=l, score=s))
    return BatchPredictResponse(items=items, count=len(items), model=getattr(svc, "model_name", "unknown"))

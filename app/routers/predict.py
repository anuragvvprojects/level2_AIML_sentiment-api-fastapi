from fastapi import APIRouter, Depends, HTTPException, Request
from app.dependencies import get_state
from app.models.schemas import PredictRequest, PredictResponse
from app.services.limiter import rate_limiter

router = APIRouter()

@router.post("/predict", response_model=PredictResponse, tags=["inference"])
def predict(payload: PredictRequest, request: Request, _rl = Depends(rate_limiter())):
    services = get_state(request)
    svc = getattr(services, "service", None) or getattr(services, "model_service", None)
    if not svc or not getattr(svc, "ready", False):
        raise HTTPException(status_code=503, detail="Model not loaded")
    label, score = svc.predict(payload.text)
    return PredictResponse(label=label, score=score, model=getattr(svc, "model_name", "unknown"), request_id=payload.request_id)

from fastapi import APIRouter
from typing import Optional

router = APIRouter()

@router.get("/version", tags=["system"])
def version(
    service_version: Optional[str] = None,
    model_name: Optional[str] = None,
    max_tokens: Optional[int] = None,
):
    """Lightweight info endpoint.
    In production, prefer wiring values from app config in app.main.
    """
    return {
        "service_version": service_version or "0.1.0",
        "model_name": model_name or "unset",
        "max_tokens": max_tokens or 256,
    }

from .health import router as health_router
from .info import router as info_router
from .predict import router as predict_router
from .batch import router as batch_router
from .explain import router as explain_router

__all__ = [
    "health_router",
    "info_router",
    "predict_router",
    "batch_router",
    "explain_router",
]

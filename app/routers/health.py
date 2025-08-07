from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["system"])
def health():
    return {"status": "ok"}

@router.get("/ready", tags=["system"])
def ready():
    # Actual readiness depends on main app wiring; return True as a default.
    return {"ready": True}

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Dict, Any
from app.dependencies import get_state
from app.services.limiter import rate_limiter

router = APIRouter()

POS_WORDS = {"good","great","love","excellent","amazing","happy","fantastic","awesome","liked","positive"}
NEG_WORDS = {"bad","terrible","hate","awful","horrible","sad","poor","worse","worst","negative"}

@router.post("/explain", tags=["inference"])
def explain(payload: Dict[str, str], request: Request, _rl = Depends(rate_limiter())) -> Dict[str, Any]:
    """Naive, dependency-free explanation:
    - tokenizes on whitespace
    - assigns +1 to simple positive words, -1 to negatives, 0 otherwise
    - returns overall naive score and per-token attributions
    This is *not* a faithful model explanation; use SHAP/Integrated Gradients in production.
    """
    text = (payload.get("text") or "").strip()
    if not text:
        raise HTTPException(status_code=422, detail="text is required")
    tokens = text.split()
    attributions = []
    score = 0
    for tok in tokens:
        t = tok.strip(".,!?;:"'()[]{}").lower()
        w = 1 if t in POS_WORDS else (-1 if t in NEG_WORDS else 0)
        attributions.append({"token": tok, "weight": w})
        score += w
    sentiment_hint = "POSITIVE" if score > 0 else ("NEGATIVE" if score < 0 else "NEUTRAL")
    return {"hint": sentiment_hint, "score": score, "tokens": attributions}

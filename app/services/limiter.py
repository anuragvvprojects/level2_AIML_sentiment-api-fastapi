import time
from collections import deque
from typing import Deque, Dict, Tuple
from fastapi import Request, HTTPException

# Sliding-window limiter (memory local). Good enough for dev & small scale.
_VISITS: Dict[str, Deque[float]] = {}

def _allow(key: str, limit: int, window_sec: int) -> Tuple[bool, float]:
    now = time.time()
    dq = _VISITS.setdefault(key, deque())
    # purge old entries
    while dq and (now - dq[0]) > window_sec:
        dq.popleft()
    if len(dq) >= limit:
        retry_after = window_sec - (now - dq[0])
        return False, max(retry_after, 0.0)
    dq.append(now)
    return True, 0.0

def rate_limiter(limit_per_minute: int = 120, window_sec: int = 60):
    """FastAPI dependency that enforces a per-client sliding-window limit."""
    def _dep(request: Request):
        key = request.headers.get("X-Client-Id") or (request.client.host if request.client else "anon")
        ok, retry_after = _allow(key, limit_per_minute, window_sec)
        if not ok:
            raise HTTPException(status_code=429, detail="rate_limited", headers={"Retry-After": str(int(retry_after)+1)})
    return _dep

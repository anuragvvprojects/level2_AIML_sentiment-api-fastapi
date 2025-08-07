import time
from collections import deque, defaultdict
from typing import Deque, DefaultDict
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory sliding-window rate limiter.

    Not distributed-safe; suitable for dev/single-instance deployments.
    Key is derived from `X-Client-Id` header or remote IP.
    """
    def __init__(self, app, limit: int = 120, window_sec: int = 60):
        super().__init__(app)
        self.limit = int(limit)
        self.window_sec = int(window_sec)
        self._visits: DefaultDict[str, Deque[float]] = defaultdict(deque)

    async def dispatch(self, request, call_next):
        key = request.headers.get("X-Client-Id") or (request.client.host if request.client else "anon")
        now = time.time()
        dq = self._visits[key]
        # drop old entries
        while dq and (now - dq[0]) > self.window_sec:
            dq.popleft()
        if len(dq) >= self.limit:
            retry_after = int(self.window_sec - (now - dq[0])) + 1
            return JSONResponse(status_code=429, content={"detail": "rate_limited"}, headers={"Retry-After": str(retry_after)})
        dq.append(now)
        return await call_next(request)

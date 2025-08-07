from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import traceback

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Catch-all error handler that converts unhandled exceptions to JSON 500s.

    It preserves FastAPI HTTPException status codes.
    """
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "detail": e.detail if isinstance(e.detail, str) else "http_error",
                },
            )
        except Exception as e:
            # Optionally log the traceback here or bind to structlog
            tb = traceback.format_exc()
            return JSONResponse(status_code=500, content={"detail": "internal_error"})

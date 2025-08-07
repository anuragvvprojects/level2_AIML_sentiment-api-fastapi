import uuid
from starlette.middleware.base import BaseHTTPMiddleware

HEADER = "X-Request-Id"

class RequestIdMiddleware(BaseHTTPMiddleware):
    """Ensures every request/response has an X-Request-Id for correlation."""
    async def dispatch(self, request, call_next):
        rid = request.headers.get(HEADER) or str(uuid.uuid4())
        request.state.request_id = rid  # available to handlers
        response = await call_next(request)
        response.headers[HEADER] = rid
        return response

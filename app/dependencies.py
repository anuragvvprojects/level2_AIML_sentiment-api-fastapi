from fastapi import Request

def get_state(request: Request):
    """Expose app.state for DI in routers."""
    return request.app.state

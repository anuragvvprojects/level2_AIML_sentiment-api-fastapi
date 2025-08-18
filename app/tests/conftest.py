import pytest

class StubService:
    def __init__(self):
        self.model_name = "stub-model"
        self.ready_flag = False

    def load(self):
        # Simulate successful model load at startup
        self.ready_flag = True

    @property
    def ready(self) -> bool:
        return self.ready_flag

    def predict(self, text: str):
        # Very simple heuristic for tests
        t = (text or "").lower()
        if "love" in t or "great" in t or "good" in t:
            return "POSITIVE", 0.99
        if "terrible" in t or "bad" in t or "refund" in t:
            return "NEGATIVE", 0.80
        return "NEUTRAL", 0.55

@pytest.fixture()
def client():
    from fastapi.testclient import TestClient
    import app.main as app_main

    # Replace the real service with a stub before TestClient triggers startup
    app_main.app.state.service = StubService()
    return TestClient(app_main.app)

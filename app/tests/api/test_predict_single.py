def test_predict_positive(client):
    payload = {"text": "I love this product!"}
    r = client.post("/predict", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["label"] in {"POSITIVE", "NEGATIVE", "NEUTRAL"}
    assert 0.0 <= body["score"] <= 1.0
    assert body["model"] == "stub-model"

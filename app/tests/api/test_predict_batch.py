def test_predict_batch(client):
    payload = {"texts": ["I love this!", "This was terrible and I want a refund."]}
    r = client.post("/predict/batch", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 2
    assert body["model"] == "stub-model"
    assert isinstance(body["items"], list) and len(body["items"]) == 2
    for item in body["items"]:
        assert "label" in item and "score" in item

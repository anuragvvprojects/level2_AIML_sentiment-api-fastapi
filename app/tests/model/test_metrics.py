import numpy as np
from model.compute_metrics import compute_metrics

def test_compute_metrics_binary():
    preds = np.array([0,1,1,0,1])
    labels = np.array([0,1,0,0,1])
    m = compute_metrics((preds, labels))
    assert 0.0 <= m["accuracy"] <= 1.0
    assert 0.0 <= m["f1_macro"] <= 1.0

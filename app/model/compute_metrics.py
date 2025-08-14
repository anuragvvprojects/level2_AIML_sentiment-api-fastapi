from typing import Dict
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

def compute_metrics(eval_pred) -> Dict[str, float]:
    preds, labels = eval_pred
    if preds.ndim > 1:
        preds = preds.argmax(axis=-1)
    acc = accuracy_score(labels, preds)
    p, r, f1, _ = precision_recall_fscore_support(labels, preds, average="macro", zero_division=0)
    return {"accuracy": acc, "precision_macro": p, "recall_macro": r, "f1_macro": f1}

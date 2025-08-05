from __future__ import annotations
from typing import List, Dict, Tuple

from transformers import pipeline

_LABEL_MAP = {
    "1": "POSITIVE",
    "2": "NEGATIVE",
    "POSITIVE": "POSITIVE",
    "NEGATIVE": "NEGATIVE",
    "NEUTRAL": "NEUTRAL",
    "LABEL_0": "NEGATIVE",
    "LABEL_1": "POSITIVE",
    "LABEL_2": "NEUTRAL",
}

def _normalize_label(label: str) -> str:
    key = (label or "").strip().upper()
    return _LABEL_MAP.get(key, key or "UNKNOWN")

class ModelService:
    """Wrapper around HF transformers pipeline for sentiment analysis."""
    def __init__(self, model_name: str, max_tokens: int = 256, device: str = "cpu"):
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.device = device
        self._pipe = None

    def load(self):
        self._pipe = pipeline(
            task="sentiment-analysis",
            model=self.model_name,
            tokenizer=self.model_name,
            truncation=True,
            max_length=self.max_tokens,
            device=-1 if self.device == "cpu" else 0,
        )

    @property
    def ready(self) -> bool:
        return self._pipe is not None

    def predict_one(self, text: str) -> Tuple[str, float]:
        if not self._pipe:
            raise RuntimeError("Pipeline not loaded")
        out = self._pipe(text, truncation=True, max_length=self.max_tokens)[0]
        return _normalize_label(str(out.get("label", ""))), float(out.get("score", 0.0))

    def predict_batch(self, texts: List[str]) -> List[Dict[str, float]]:
        if not self._pipe:
            raise RuntimeError("Pipeline not loaded")
        outs = self._pipe(texts, truncation=True, max_length=self.max_tokens)
        result = []
        for o in outs:
            result.append({"label": _normalize_label(str(o.get("label", ""))), "score": float(o.get("score", 0.0))})
        return result

from __future__ import annotations
from transformers import AutoTokenizer

class TokenizerService:
    def __init__(self, model_name: str, max_length: int = 256):
        self.model_name = model_name
        self.max_length = max_length
        self._tok = None

    def load(self):
        self._tok = AutoTokenizer.from_pretrained(self.model_name)

    @property
    def ready(self) -> bool:
        return self._tok is not None

    def encode(self, text: str):
        if not self._tok:
            raise RuntimeError("Tokenizer not loaded")
        return self._tok(
            text,
            truncation=True,
            max_length=self.max_length,
            padding=False,
            return_tensors="pt",
        )

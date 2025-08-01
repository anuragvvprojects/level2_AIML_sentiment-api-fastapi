from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

from .types import SentimentLabel

MAX_TEXT_LEN = 5000  # keep payloads reasonable for API use

class PredictRequest(BaseModel):
    text: str = Field(..., description="Input text for sentiment classification", max_length=MAX_TEXT_LEN)
    request_id: Optional[str] = Field(default=None, description="Optional correlation id")

    @field_validator("text")
    @classmethod
    def _non_empty(cls, v: str) -> str:
        v2 = (v or "").strip()
        if not v2:
            raise ValueError("text must be non-empty")
        return v2

class PredictResponse(BaseModel):
    label: SentimentLabel = Field(..., description="Predicted sentiment label")
    score: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0..1)")
    model: str = Field(..., description="Model identifier used for inference")
    request_id: Optional[str] = None

class BatchPredictRequest(BaseModel):
    texts: List[str] = Field(..., description="List of input strings")

    @field_validator("texts")
    @classmethod
    def _validate_texts(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("texts must contain at least one item")
        cleaned = []
        for t in v:
            t2 = (t or "").strip()
            if not t2:
                raise ValueError("texts must not contain empty strings")
            if len(t2) > MAX_TEXT_LEN:
                raise ValueError(f"text length exceeds {MAX_TEXT_LEN} characters")
            cleaned.append(t2)
        return cleaned

class BatchPredictResponseItem(BaseModel):
    label: SentimentLabel
    score: float = Field(..., ge=0.0, le=1.0)

class BatchPredictResponse(BaseModel):
    items: List[BatchPredictResponseItem]
    count: int
    model: str

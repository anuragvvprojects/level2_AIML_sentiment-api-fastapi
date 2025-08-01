from enum import Enum

class SentimentLabel(str, Enum):
    """Normalized label space for sentiment outputs.

    Most binary models use {POSITIVE, NEGATIVE}. Some tri-class models add NEUTRAL.
    """
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"

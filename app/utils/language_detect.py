import re
from typing import Literal

Lang = Literal["en","es","fr","de","ru","ar","hi","zh","other"]

# Heuristic script ranges
RE_CYRILLIC = re.compile(r"[\u0400-\u04FF]")
RE_ARABIC   = re.compile(r"[\u0600-\u06FF]")
RE_DEVANAG  = re.compile(r"[\u0900-\u097F]")
RE_HAN      = re.compile(r"[\u4E00-\u9FFF]")

# Quick bigram hints (very rough)
HINTS = {
    "es": [" que ", " de ", " la ", " el ", " y "],
    "fr": [" le ", " la ", " et ", " de ", " que "],
    "de": [" der ", " die ", " und ", " ist "],
    "en": [" the ", " and ", " is "],
}

def detect_language(text: str) -> Lang:
    \"\"\"Very lightweight language detection heuristic.
    Prefer using a real library in production; this is dependency-free.

    Returns one of: en, es, fr, de, ru, ar, hi, zh, other
    \"\"\"
    t = f" {text.lower()} "
    if RE_CYRILLIC.search(t):
        return "ru"
    if RE_ARABIC.search(t):
        return "ar"
    if RE_DEVANAG.search(t):
        return "hi"
    if RE_HAN.search(t):
        return "zh"

    # Latin-based rough hints
    scores = {k: 0 for k in HINTS}
    for lang, needles in HINTS.items():
        for n in needles:
            if n in t:
                scores[lang] += 1
    if scores:
        best = max(scores, key=scores.get)
        if scores[best] > 0:
            return best  # type: ignore

    return "other"

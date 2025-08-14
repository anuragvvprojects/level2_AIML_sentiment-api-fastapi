from typing import Dict
from datasets import load_dataset
from transformers import AutoTokenizer

def tokenize(name: str = "imdb", model_name: str = "distilbert-base-uncased", max_length: int = 256) -> Dict:
    tok = AutoTokenizer.from_pretrained(model_name)
    ds = load_dataset(name)
    def _map(ex):
        return tok(ex["text"], truncation=True, max_length=max_length)
    return ds.map(_map, batched=True)

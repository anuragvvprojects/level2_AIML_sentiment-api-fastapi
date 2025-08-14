from typing import Tuple
from datasets import load_dataset  # pip install datasets
from sklearn.model_selection import train_test_split

def load_imdb(split_ratio: float = 0.2, seed: int = 42) -> Tuple[list[str], list[int], list[str], list[int]]:
    ds = load_dataset("imdb")
    X = [x["text"] for x in ds["train"]]
    y = [x["label"] for x in ds["train"]]
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=split_ratio, random_state=seed, stratify=y)
    return X_train, y_train, X_val, y_val

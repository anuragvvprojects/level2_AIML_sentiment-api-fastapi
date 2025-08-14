import os, json, numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline

MODEL_ID = os.getenv("MODEL_NAME", "distilbert-base-uncased-finetuned-sst-2-english")
EXAMPLES = [
    "I absolutely loved this product — works great!",
    "This was terrible and I want a refund."
]

def main():
    tok = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)
    pipe = TextClassificationPipeline(model=model, tokenizer=tok, top_k=None, function_to_apply="softmax")
    for t in EXAMPLES:
        res = pipe(t)[0]
        if isinstance(res, list):  # handle top_k list
            res = max(res, key=lambda x: x["score"])
        print(json.dumps({"text": t, "label": res["label"], "score": float(res["score"])}, ensure_ascii=False))

if __name__ == "__main__":
    main()

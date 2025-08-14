import time, statistics, json, os
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline

MODEL = os.getenv("MODEL_NAME", "distilbert-base-uncased-finetuned-sst-2-english")
N = int(os.getenv("N", "50"))
TEXT = "I absolutely love this!"

def main():
    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    pipe = TextClassificationPipeline(model=model, tokenizer=tok)
    lat = []
    for _ in range(N):
        t0 = time.perf_counter()
        _ = pipe(TEXT)
        lat.append(1000*(time.perf_counter()-t0))
    print(json.dumps({"p50_ms": statistics.median(lat), "p95_ms": sorted(lat)[int(0.95*len(lat))-1]}, indent=2))

if __name__ == "__main__":
    main()

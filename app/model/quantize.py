import os, torch
from transformers import AutoModelForSequenceClassification

MODEL_ID = os.getenv("MODEL_NAME", "distilbert-base-uncased-finetuned-sst-2-english")
OUT = "model/artifacts/quantized.pt"

def main():
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID).cpu()
    qmodel = torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
    torch.save(qmodel.state_dict(), OUT)
    print("Saved quantized weights ->", OUT)

if __name__ == "__main__":
    main()

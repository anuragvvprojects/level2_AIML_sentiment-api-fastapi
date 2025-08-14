import os
from transformers.onnx import export, FeaturesManager
from transformers import AutoConfig, AutoTokenizer
from pathlib import Path

MODEL_ID = os.getenv("MODEL_NAME", "distilbert-base-uncased-finetuned-sst-2-english")
OUT = Path("model/artifacts/onnx")

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    task = "sequence-classification"
    config = AutoConfig.from_pretrained(MODEL_ID)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model_kind, onnx_config = FeaturesManager.check_supported_model_or_raise(config, feature=task)
    onnx_config = onnx_config(model_kind, config)
    export(tokenizer, onnx_config, MODEL_ID, OUT / "model.onnx")

if __name__ == "__main__":
    main()

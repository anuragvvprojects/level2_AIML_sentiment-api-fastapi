import os
from dataclasses import dataclass
from datasets import load_dataset
from transformers import (AutoTokenizer, AutoModelForSequenceClassification,
                          DataCollatorWithPadding, TrainingArguments, Trainer)
from .compute_metrics import compute_metrics

@dataclass
class TrainConfig:
    model_name: str = os.getenv("MODEL_NAME", "distilbert-base-uncased")
    dataset: str = os.getenv("DATASET", "imdb")
    num_labels: int = int(os.getenv("NUM_LABELS", "2"))
    epochs: int = int(os.getenv("EPOCHS", "1"))
    lr: float = float(os.getenv("LR", "5e-5"))
    batch_size: int = int(os.getenv("BATCH_SIZE", "8"))
    max_length: int = int(os.getenv("MAX_TOKENS", "256"))
    out_dir: str = os.getenv("OUT_DIR", "model/artifacts/hf")

def main():
    cfg = TrainConfig()
    tok = AutoTokenizer.from_pretrained(cfg.model_name)
    ds = load_dataset(cfg.dataset)

    def _preprocess(ex):
        return tok(ex["text"], truncation=True, max_length=cfg.max_length)

    ds = ds.map(_preprocess, batched=True)
    model = AutoModelForSequenceClassification.from_pretrained(cfg.model_name, num_labels=cfg.num_labels)
    collator = DataCollatorWithPadding(tokenizer=tok)
    args = TrainingArguments(
        output_dir=cfg.out_dir,
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=cfg.lr,
        per_device_train_batch_size=cfg.batch_size,
        per_device_eval_batch_size=cfg.batch_size,
        num_train_epochs=cfg.epochs,
        logging_steps=50,
    )
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=ds["train"],
        eval_dataset=ds.get("test") or ds.get("validation"),
        data_collator=collator,
        tokenizer=tok,
        compute_metrics=compute_metrics,
    )
    trainer.train()
    trainer.save_model(cfg.out_dir)
    print("Saved model to", cfg.out_dir)

if __name__ == "__main__":
    main()

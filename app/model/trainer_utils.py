from transformers import DataCollatorWithPadding

def build_data_collator(tokenizer):
    return DataCollatorWithPadding(tokenizer=tokenizer)

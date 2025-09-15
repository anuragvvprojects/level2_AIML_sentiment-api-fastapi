from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig

model_id = "mistralai/Mistral-7B-Instruct-v0.1"

# Quantization config: 4-bit with optimized settings
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype="float16",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

print("🔍 Loading model...")
tokenizer = AutoTokenizer.from_pretrained(model_id)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    quantization_config=quant_config,
    torch_dtype="auto"
)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

prompt = "What is a force majeure clause in a legal contract?"
print("🧠 Generating...")
out = pipe(prompt, max_new_tokens=150)
print("💬 Response:", out[0]["generated_text"])

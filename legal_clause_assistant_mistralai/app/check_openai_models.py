import os
import openai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in environment variables or .env file.")

openai.api_key = api_key

try:
    models = openai.models.list()
    print("✅ Available models under your API key:")
    for model in sorted([m.id for m in models.data if "gpt" in m.id]):
        print("  •", model)
except Exception as e:
    print("❌ Error while fetching models:", e)

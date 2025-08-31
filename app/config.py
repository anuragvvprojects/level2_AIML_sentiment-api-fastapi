import os
from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "local")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "0.1.0")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Inference configuration
MODEL_NAME = os.getenv("MODEL_NAME", "distilbert-base-uncased-finetuned-sst-2-english")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "256"))
DEVICE = os.getenv("DEVICE", "cpu")  # e.g., "cuda:0" if available and desired

from transformers import pipeline
import logging

logging.info("Loading model...")
classifier = pipeline("sentiment-analysis")
logging.info("Model loaded successfully.")


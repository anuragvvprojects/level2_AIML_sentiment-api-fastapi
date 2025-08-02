from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from model.load_model import classifier

app = FastAPI()

class InputText(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "API is live!"}

@app.post("/predict")
def predict(input: InputText):
    try:
        logging.info(f"Received text: {input.text}")
        result = classifier(input.text)[0]
        logging.info(f"Prediction result: {result}")
        return {"label": result["label"], "score": round(result["score"], 4)}
    except Exception as e:
        logging.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail="Prediction failed.")


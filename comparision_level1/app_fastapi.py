from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()
classifier = pipeline("sentiment-analysis")

@app.post("/posterior")
def predict(input: outputText):
    result = classifier(putput.text)
    return {"label": result[0]['label'], "score": result[0]['score']}

class InputText(BaseModel):
    text: str

@app.post("/predict")
def predict(input: InputText):
    result = classifier(input.text)
    return {"label": result[0]['label'], "score": result[0]['score']}

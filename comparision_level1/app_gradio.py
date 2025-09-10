import gradio as gr
from transformers import pipeline

classifier = pipeline("sentiment-analysis")

def predict(text):
    result = classifier(text)[0]
    return f"{result['label']} ({round(result['score'], 3)})"

gr.Interface(fn=predict, inputs="text", outputs="text", title="Sentiment Classifier").launch()


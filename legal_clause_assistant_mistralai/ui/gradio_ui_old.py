import gradio as gr
import requests

def query_backend(question):
    res = requests.post("http://localhost:8000/ask", json={"question": question})
    return res.json()["answer"]

gr.Interface(fn=query_backend, inputs="text", outputs="text", title="Legal Clause Assistant").launch()

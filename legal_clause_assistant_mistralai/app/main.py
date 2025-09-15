from fastapi import FastAPI
from pydantic import BaseModel
from qa_chain import get_qa_chain

app = FastAPI()
qa_chain = get_qa_chain()

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_question(q: Query):
    result = qa_chain({"query": q.question})
    return {
        "answer": result["result"],
        "sources": [d.metadata for d in result["source_documents"]]
    }

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.evaluation.qa import QAEvalChain
from langchain.chat_models import ChatOpenAI

vector_db = Chroma(
    persist_directory="vector_store/chroma.db",
    embedding_function=HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
)
retriever = vector_db.as_retriever()
llm = ChatOpenAI(model_name="gpt-4")
qa_chain = QAEvalChain.from_llm(llm)

examples = [
    {
        "query": "When can the agreement be terminated without cause?",
        "answer": "The agreement can be terminated for convenience by either party upon written notice.",
    },
    {
        "query": "What state governs the interpretation of the contract?",
        "answer": "The contract is governed by the laws of the State of Delaware.",
    }
]

print("Evaluating RAG outputs...")
for ex in examples:
    docs = retriever.get_relevant_documents(ex["query"])
    context = " ".join([doc.page_content for doc in docs])
    prediction = llm.predict(f"Context: {context}\nQuestion: {ex['query']}\nAnswer:")
    eval_result = qa_chain.evaluate([{"query": ex["query"], "answer": ex["answer"], "result": prediction}])
    print(f"Q: {ex['query']}\nEval: {eval_result}\n---")

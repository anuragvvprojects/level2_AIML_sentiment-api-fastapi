from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a legal assistant. Use the context below to answer the question. 
Cite clause types if relevant. If unsure, say you don’t know.

Context:
{context}

Question: {question}

Answer:
"""
)

def get_qa_chain():
    vector_db = Chroma(
        persist_directory="vector_store/chroma.db",
        embedding_function=HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
    )
    retriever = vector_db.as_retriever(search_kwargs={"k": 5})
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": QA_PROMPT},
        return_source_documents=True
    )
    return chain

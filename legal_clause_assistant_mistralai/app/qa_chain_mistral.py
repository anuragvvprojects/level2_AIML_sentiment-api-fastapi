from langchain.chains import RetrievalQA  # <- keep this from core
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig

VECTOR_DB_DIR = "vector_store"
EMBED_MODEL_NAME = "BAAI/bge-base-en-v1.5"
LLM_MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"

def get_qa_chain():
    # Load vector store
    vector_db = Chroma(
        persist_directory=VECTOR_DB_DIR,
        embedding_function=HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
    )

    retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_NAME)

    bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_use_double_quant=True, bnb_4bit_quant_type="nf4")
    model = AutoModelForCausalLM.from_pretrained(LLM_MODEL_NAME, device_map="auto", quantization_config=bnb_config)

    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=512, temperature=0.2)
    llm = HuggingFacePipeline(pipeline=pipe)

    # Create prompt template
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are a legal assistant. Use the following context to answer the legal question.
If the answer is not in the context, say so.

Context:
{context}

Question:
{question}

Answer:"""
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt_template},
        return_source_documents=False,
    )

    return qa_chain

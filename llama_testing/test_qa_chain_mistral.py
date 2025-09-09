from qa_chain_mistral import get_qa_chain

def test_query():
    qa_chain = get_qa_chain()
    query = "What is the governing law in the contract?"
    response = qa_chain.invoke({"query": query})
    print("💬 Question:", query)
    print("🧠 Answer:", response["result"])

if __name__ == "__main__":
    test_query()

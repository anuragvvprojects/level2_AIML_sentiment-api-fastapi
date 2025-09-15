from qa_chain import get_qa_chain

def test_query():
    qa_chain = get_qa_chain()

    query = "When can the agreement be terminated without cause?"
    response = qa_chain({"query": query})

    print("🧠 Question:", query)
    print("📝 Answer:", response["result"])
    print("\n📚 Source Metadata (1st result):")
    print(response["source_documents"][0].metadata)

if __name__ == "__main__":
    test_query()

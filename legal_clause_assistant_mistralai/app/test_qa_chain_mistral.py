from qa_chain_mistral import get_qa_chain

def test_query():
    qa_chain = get_qa_chain()
    query = "What are the IP ownership terms in the agreement?"
    query = "What does the agreement say about license grant?"
    query = "Who owns the jointly developed IP in this agreement?"
    query = "Summarize the exclusivity clause in the agreement."
    # Manually run retriever
    retriever = qa_chain.retriever
    docs = retriever.get_relevant_documents(query)
    
    print("\n📄 Retrieved Context:")
    for i, doc in enumerate(docs[:3]):
        print(f"\n--- Document #{i+1} ---\n{doc.page_content[:1000]}")

    # Run actual QA
    response = qa_chain.invoke({"query": query})
    print("\n🧠 Answer:")
    print(response["result"])
    
if __name__ == "__main__":
    test_query()

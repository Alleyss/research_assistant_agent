def get_prompt_1(question, context):
    PROMTP_1 = (
        "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.",
        f"Question: {question}",
        f"Context: {context}",
        "Answer:",
    )

    return PROMTP_1


def generate(question, llm, context):
    docs_content = "\n\n".join(doc.page_content for doc in context)
    messages = get_prompt_1(question=question, context=docs_content)
    response = llm.invoke(messages)
    return {"answer": response.content}

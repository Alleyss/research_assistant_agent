from langchain_core.vectorstores import InMemoryVectorStore


def init_vector_store(embedding_model):
    global vector_store
    vector_store = InMemoryVectorStore(embedding_model)


def add_pdfdocument_to_vector(data):
    vector_store.add_documents(data)


def retrieve_pdfdocument_from_vector(state):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}

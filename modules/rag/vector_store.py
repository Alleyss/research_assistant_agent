from langchain_core.vectorstores import InMemoryVectorStore
import os

session_vector_stores = {}


def init_vector_store(session_id, embedding_model):
    global session_vector_stores

    if session_id not in session_vector_stores:
        session_vector_stores[session_id] = InMemoryVectorStore(embedding_model)

    return session_vector_stores[session_id]


def clear_vector_store(session_id):
    global session_vector_stores

    if session_id in session_vector_stores:
        del session_vector_stores[session_id]


def add_pdfdocument_to_vector(session_id, data):
    global session_vector_stores

    if session_id in session_vector_stores:
        session_vector_stores[session_id].add_documents(data)


def retrieve_pdfdocument_from_vector(session_id, question, k=4):
    global session_vector_stores

    if session_id in session_vector_stores:
        retrieved_docs = session_vector_stores[session_id].similarity_search(
            question, k=k
        )
        return {"context": retrieved_docs}

    return {"context": []}

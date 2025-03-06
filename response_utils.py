from utils.preprocessing import get_gemini_api_key, get_gemini_llm, pdf_loader
from modules.pdf_processor import get_pdf_elements
from modules.embeddings import get_embedding_model, pdf_chunkify
from modules.vector_store import (
    add_pdfdocument_to_vector,
    retrieve_pdfdocument_from_vector,
    init_vector_store,
    clear_vector_store,
)
from modules.llm_generate import generate


def init_model_in_memory():
    ## GEMINI API
    GEMINI_API = get_gemini_api_key()
    llm = get_gemini_llm(GEMINI_API)
    ## EMBEDDINGS
    embedding_model = get_embedding_model()
    return llm, embedding_model


def set_pdf_in_memory(session_id, pdf_path, embedding_model):
    pdf_docs = pdf_loader(pdf_path)
    pdf_chunks = pdf_chunkify(pdf_docs)

    ## VECTOR STORE
    init_vector_store(session_id, embedding_model)
    add_pdfdocument_to_vector(session_id, pdf_chunks)    
    print(f"Adding PDF to vector store : {pdf_path}")



def get_chat_response(user_message, llm, context):
    response = generate(user_message, llm, context)
    return response['answer']


def rebuild_session_vector_store(session_id, pdf_files, embedding_model):
    clear_vector_store(session_id)
    print(f"Rebuilding session vector store id : {session_id}")

    # Create a new vector store
    init_vector_store(session_id, embedding_model)

    # Add each PDF to the vector store
    for pdf_path in pdf_files:
        set_pdf_in_memory(session_id, pdf_path, embedding_model)

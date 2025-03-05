from utils.preprocessing import get_gemini_api_key, get_gemini_llm, pdf_loader
from modules.pdf_processor import get_pdf_elements
from modules.embeddings import get_embedding_model, pdf_chunkify
from modules.vector_store import (
    add_pdfdocument_to_vector,
    retrieve_pdfdocument_from_vector,
    init_vector_store,
)
from modules.llm_generate import generate


def init_model_in_memory():
    ## GEMINI API
    GEMINI_API = get_gemini_api_key()
    llm = get_gemini_llm(GEMINI_API)
    ## EMBEDDINGS
    embedding_model = get_embedding_model()
    return llm, embedding_model


def set_pdf_in_memory(PDF_FILE_PATH, embedding_model):
    pdf_docs = pdf_loader(PDF_FILE_PATH)
    pdf_chunks = pdf_chunkify(pdf_docs)

    ## VECTOR STORE
    init_vector_store(embedding_model)
    add_pdfdocument_to_vector(pdf_chunks)


def get_chat_response(user_message, llm):
    state = {"question": user_message}
    response = retrieve_pdfdocument_from_vector(state)
    ## LLM GENERATE
    state["context"] = response["context"]
    response = generate(state, llm)
    return response["answer"]

    ## OUTPUT
    # print(f'Question : {state["question"]}')
    # print(f'Answer : {state["answer"]}')

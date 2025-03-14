from utils.preprocessing import get_gemini_api_key, get_gemini_llm, pdf_loader
from modules.rag.pdf_processor import get_pdf_elements
from modules.rag.embeddings import get_embedding_model, pdf_chunkify
from modules.rag.vector_store import (
    add_pdfdocument_to_vector,
    retrieve_pdfdocument_from_vector,
    init_vector_store,
)
from modules.rag.llm_generate import generate

GEMINI_API = get_gemini_api_key()
llm = get_gemini_llm(GEMINI_API)


PDF_PATH = "cache_files/pdfs/ace.pdf"
pdf_docs = pdf_loader(PDF_PATH)

## EMBEDDINGS
embedding_model = get_embedding_model()
pdf_chunks = pdf_chunkify(pdf_docs)

## VECTOR STORE
init_vector_store(embedding_model)
add_pdfdocument_to_vector(pdf_chunks)
state = {"question": "What is the syllabus of associate cloud engineer exam"}
response = retrieve_pdfdocument_from_vector(state)
# print(response)

## LLM GENERATE
state["context"] = response["context"]
response = generate(state, llm)
state["answer"] = response["answer"]

## OUTPUT
print(f'Question : {state["question"]}')
print(f'Answer : {state["answer"]}')
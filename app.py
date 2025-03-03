from utils.preprocessing import get_gemini_api_key, get_gemini_llm
from modules.pdf_processor import get_pdf_elements
from modules.embeddings import generate_embeddings
GEMINI_API = get_gemini_api_key()
engine = get_gemini_llm(GEMINI_API)
# print(engine.invoke("Hello, what is your name?").content)


data = get_pdf_elements("cache_files/pdfs/ace.pdf")
# for element in data:
#     print(element)
#     print("\n")

embeddings=generate_embeddings(data)
for em in embeddings:
    print(em)
    print("\n")
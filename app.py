from utils.preprocessing import get_gemini_api_key, get_gemini_llm
from modules.pdf_processor import extract_text_from_pdf, clean_text

GEMINI_API = get_gemini_api_key()
engine = get_gemini_llm(GEMINI_API)
# print(engine.invoke("Hello, what is your name?").content)

#1 PDF Extraction
raw_text=extract_text_from_pdf("ace.pdf")
cleaned_text=clean_text(raw_text)
print(cleaned_text[:500]) #first 500 characters
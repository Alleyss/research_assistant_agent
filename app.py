from utils.preprocessing import get_gemini_api_key, get_qa_engine


GEMINI_API = get_gemini_api_key()
engine = get_qa_engine(GEMINI_API)
print(engine)

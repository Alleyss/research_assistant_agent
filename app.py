from utils.preprocessing import get_gemini_api_key, get_gemini_llm


GEMINI_API = get_gemini_api_key()
engine = get_gemini_llm(GEMINI_API)
print(engine.invoke("Hello, what is your name?").content)
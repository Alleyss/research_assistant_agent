import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def get_gemini_api_key() -> str:
    return os.getenv("GEMINI_API_KEY")


def get_gemini_llm(API_KEY) -> ChatGoogleGenerativeAI:
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=API_KEY)
    return llm

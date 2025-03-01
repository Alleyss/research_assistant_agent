import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def get_gemini_api_key() -> str:
    return os.getenv("GEMINI_API_KEY")


def get_qa_engine(API_KEY) -> ChatGoogleGenerativeAI:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", api_key=API_KEY)
    return llm

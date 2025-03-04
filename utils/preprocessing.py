import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_unstructured import UnstructuredLoader

load_dotenv()


def get_gemini_api_key() -> str:
    return os.getenv("GEMINI_API_KEY")


def get_gemini_llm(API_KEY) -> ChatGoogleGenerativeAI:
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=API_KEY)
    return llm


def pdf_loader(pdf_filepath: str):
    loader = UnstructuredLoader(
        file_path=pdf_filepath,
        chunking_strategy="basic",
        max_characters=1000000,
        include_orig_elements=False,
    )

    return loader.load()

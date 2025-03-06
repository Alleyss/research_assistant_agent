from utils.preprocessing import get_gemini_api_key
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_embedding_model():
    """Initializes the Gemini Embeddings model."""
    api_key = get_gemini_api_key()
    embedding_model = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", google_api_key=api_key
    )
    return embedding_model


def pdf_chunkify(pdf_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_splits = text_splitter.split_documents(pdf_data)
    return all_splits

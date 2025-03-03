from utils.preprocessing import get_gemini_api_key
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def generate_embeddings(chunks_list):
    """Generates embeddings for a list of text chunks using Gemini Embeddings."""
    api_key=get_gemini_api_key()
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    embeddings = [embedding_model.embed_query(chunk.text) for chunk in chunks_list]  # Extract text from elements
    return embeddings



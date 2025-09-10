# models/llm.py
from config.config import GROQ_API_KEY
from langchain_groq import ChatGroq

def get_chat_model():
    """
    Returns a Groq chat model.
    """
    if not GROQ_API_KEY:
        raise ValueError("Missing GROQ_API_KEY in .env file")

    return ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model="llama-3.1-8b-instant"  # ✅ Groq fast model
    )

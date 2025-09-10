import os
from pathlib import Path

# Only needed locally, ignore on Streamlit Cloud
try:
    from dotenv import load_dotenv
    ROOT = Path(__file__).resolve().parent.parent
    dotenv_path = ROOT / ".env"
    if dotenv_path.exists():
        load_dotenv(str(dotenv_path))
except ModuleNotFoundError:
    pass  # skip dotenv if not installed in cloud



  # e.g., for the web search tool
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
WEBSEARCH_API_KEY = os.getenv("WEBSEARCH_API_KEY", "")

def require_key(env_name: str) -> str:
    val = os.getenv(env_name)
    if not val:
        raise EnvironmentError(f"Missing required environment variable: {env_name}")
    return val

# Example helper to choose the preferred provider (optional)
def get_preferred_provider():
    if GROQ_API_KEY:
        return "groq"
    if OPENAI_API_KEY:
        return "openai"
    if GEMINI_API_KEY:
        return "gemini"
    return None

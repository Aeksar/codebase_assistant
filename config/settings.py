from dotenv import load_dotenv
import os


load_dotenv()

class Settings:
    EMBEDDINGS_MODEL = "intfloat/multilingual-e5-base"
    LLM_MODELS = "mistral-large-latest"
    PROMPT_MODELS = "rlm/rag-prompt"
    DATA_DIR = "./data"

    MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")
    QDRANT_URL = os.environ.get("QDRANT_URL")
    GITHIB_API_KEY = os.environ.get("GITHIB_API_KEY")

cfg = Settings()
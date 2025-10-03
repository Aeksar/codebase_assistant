from dotenv import load_dotenv
import os


load_dotenv()

class Settings:
    EMBEDDINGS_MODEL = "microsoft/codebert-base"
    LLM_MODELS = "mistral-large-latest"

    MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")
    QDRANT_URL = os.environ.get("QDRANT_URL")
    GITHUB_API_KEY = os.environ.get("GITHIB_API_KEY")

cfg = Settings()
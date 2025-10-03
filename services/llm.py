from langchain_mistralai import ChatMistralAI
from langchain_core.language_models import BaseLLM

from config import cfg


def get_llm() -> BaseLLM:
    return ChatMistralAI(
        model=cfg.LLM_MODELS,
        temperature=0,
        mistral_api_key=cfg.MISTRAL_API_KEY
    )
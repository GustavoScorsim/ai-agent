import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
API_KEY = os.getenv("OPENROUTER_API_KEY")


def get_llm(temperature: float = 0) -> ChatOpenAI:
    """Modelo de chat (ex.: openai/gpt-4o-mini) via OpenRouter."""
    return ChatOpenAI(
        model=os.getenv("MODEL_NAME", "openai/gpt-4o-mini"),
        api_key=API_KEY,
        base_url=BASE_URL,
        temperature=temperature,
    )


def get_embeddings() -> OpenAIEmbeddings:
    """Modelo de embeddings via OpenRouter."""
    return OpenAIEmbeddings(
        model=os.getenv("EMBEDDING_MODEL", "openai/text-embedding-3-small"),
        api_key=API_KEY,
        base_url=BASE_URL,
        check_embedding_ctx_length=False,
    )
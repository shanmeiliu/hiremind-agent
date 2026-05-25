from langchain_core.language_models.chat_models import BaseChatModel

from app.core.config import settings


def get_llm() -> BaseChatModel:
    if settings.LLM_PROVIDER == "ollama":
        from langchain_community.chat_models import ChatOllama

        return ChatOllama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0,
        )

    if settings.LLM_PROVIDER == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=0,
            api_key=settings.OPENAI_API_KEY,
        )

    if settings.LLM_PROVIDER == "openai_compatible":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=settings.OPENAI_COMPATIBLE_MODEL,
            temperature=0,
            api_key=settings.OPENAI_COMPATIBLE_API_KEY,
            base_url=settings.OPENAI_COMPATIBLE_BASE_URL,
        )

    raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")
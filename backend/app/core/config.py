import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai_compatible")
    DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/hiremind_db",
    )
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    OPENAI_COMPATIBLE_BASE_URL: str = os.getenv(
        "OPENAI_COMPATIBLE_BASE_URL",
        "https://domain.com/api/v1",
    )
    OPENAI_COMPATIBLE_API_KEY: str | None = os.getenv("OPENAI_COMPATIBLE_API_KEY")
    OPENAI_COMPATIBLE_MODEL: str = os.getenv(
        "OPENAI_COMPATIBLE_MODEL",
        "qwen2.5:7b",
    )


settings = Settings()
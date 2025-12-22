from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    chat_model: str = os.getenv("OLLAMA_CHAT_MODEL", "llama3.2")
    embed_model: str = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")

    chroma_persist_dir: str = os.getenv("CHROMA_PERSIST_DIR", "./vector_store/chroma_db")
    data_dir: str = os.getenv("DATA_DIR", "./data")


def get_settings() -> Settings:
    return Settings()

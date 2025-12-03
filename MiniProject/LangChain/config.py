# config.py — Ollama Local LLM 버전
from pathlib import Path

# ===============================
# PDF 저장 경로
# ===============================
PDF_DIR = Path("data/")

# ===============================
# Chroma 벡터 DB 경로
# ===============================
CHROMA_PERSIST_DIR = Path("data/chroma_db")

# ===============================
# 임베딩 모델 설정 (SentenceTransformer)
# ===============================
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ===============================
# Retriever 설정
# ===============================
RETRIEVER_TOP_K = 3

# ===============================
# LLM 설정 (Ollama 모델 이름)
# ===============================
# OpenAI API는 사용하지 않음.
# app.py에서 사용자가 Streamlit에서 입력
DEFAULT_OLLAMA_MODEL = "qwen2.5"

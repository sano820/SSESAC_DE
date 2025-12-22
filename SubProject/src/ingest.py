from __future__ import annotations

from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

from src.config import Settings


def load_pdf_documents(data_dir: str) -> List[Document]:
    data_path = Path(data_dir)
    pdf_files = sorted(data_path.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in: {data_path.resolve()}")

    docs: List[Document] = []
    for pdf in pdf_files:
        loader = PyPDFLoader(str(pdf))
        pages = loader.load()  # page 단위 Document 리스트
        # 메타데이터 보강
        for d in pages:
            d.metadata.setdefault("source", pdf.name)
            # pypdfloader는 보통 page=0부터 들어있음
            d.metadata.setdefault("page", d.metadata.get("page", None))
            d.metadata.setdefault("campus", "korea_univ_sejong")
        docs.extend(pages)

    return docs


def split_documents(docs: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=80,
        separators=["\n\n", "\n", " ", ""],
    )
    return splitter.split_documents(docs)


def build_or_update_chroma(
    chunks: List[Document],
    settings: Settings,
    collection_name: str = "ku_sejong_admissions",
) -> None:
    embeddings = OllamaEmbeddings(
        model=settings.embed_model,
        base_url=settings.ollama_base_url,
    )

    persist_dir = settings.chroma_persist_dir
    Path(persist_dir).mkdir(parents=True, exist_ok=True)

    # 간단히: 매번 from_documents로 "재생성" (MVP)
    # 운영형이면 "업서트/증분 인덱싱"으로 바꾸면 됨.
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir,
        collection_name=collection_name,
    )


def run_ingest(settings: Settings) -> None:
    docs = load_pdf_documents(settings.data_dir)
    chunks = split_documents(docs)
    build_or_update_chroma(chunks, settings)
    print(f"[OK] Ingest complete. chunks={len(chunks)} persist_dir={settings.chroma_persist_dir}")


if __name__ == "__main__":
    from src.config import get_settings
    run_ingest(get_settings())

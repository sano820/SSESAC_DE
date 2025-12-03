# ingest.py
# PDF들을 읽어 임베딩 생성 후 Chroma 벡터 DB에 저장합니다.

import argparse
from pathlib import Path
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from utils import load_pdfs_from_directory, split_docs
import config


def main(pdf_dir: str = None, persist_dir: str = None):
    # 경로 설정: 인자 또는 config 파일 사용
    pdf_dir = Path(pdf_dir) if pdf_dir else config.PDF_DIR
    persist_dir = Path(persist_dir) if persist_dir else config.CHROMA_PERSIST_DIR

    print(f"Loading PDFs from: {pdf_dir}")
    docs = load_pdfs_from_directory(pdf_dir)
    print(f"Loaded {len(docs)} page-documents from PDFs")

    print("Splitting documents into chunks...")
    # chunk_size와 chunk_overlap은 config 파일에서 관리될 수 있지만,
    # utils.py에서 기본값 1000/200으로 사용하도록 했습니다.
    chunks = split_docs(docs) 
    print(f"Total chunks: {len(chunks)}")

    print("Creating embeddings (SentenceTransformer) ...")
    # SentenceTransformer 임베딩 모델 로드
    embed = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)

    print(f"Persisting Chroma DB to: {persist_dir}")
    # Chroma 벡터 DB 생성 및 영구 저장
    vectordb = Chroma.from_documents(
        documents=chunks, # chunks 리스트를 직접 전달
        embedding=embed,
        persist_directory=str(persist_dir),
    )
    vectordb.persist()
    print("Ingestion complete.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf_dir", required=False, help="PDF directory (optional)")
    parser.add_argument("--persist_dir", required=False, help="Chroma persist dir (optional)")
    args = parser.parse_args()
    main(args.pdf_dir, args.persist_dir)
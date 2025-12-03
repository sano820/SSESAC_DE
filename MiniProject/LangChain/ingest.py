# ingest.py — read local PDFs, create embeddings, persist Chroma DB

import argparse
from pathlib import Path
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from utils import load_pdfs_from_directory, split_docs
import config


def main(pdf_dir: str = None, persist_dir: str = None):
    pdf_dir = Path(pdf_dir) if pdf_dir else config.PDF_DIR
    persist_dir = Path(persist_dir) if persist_dir else config.CHROMA_PERSIST_DIR

    print(f"[ingest] Loading PDFs from: {pdf_dir}")
    docs = load_pdfs_from_directory(pdf_dir)
    print(f"[ingest] Loaded {len(docs)} page-documents from PDFs")

    print("[ingest] Splitting documents into chunks...")
    chunks = split_docs(docs)
    print(f"[ingest] Total chunks: {len(chunks)}")

    print("[ingest] Creating embeddings...")
    embed = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)

    print(f"[ingest] Persisting Chroma DB to: {persist_dir}")
    persist_dir.mkdir(parents=True, exist_ok=True)

    vectordb = Chroma.from_documents(
        # documents=chunks,
        chunks,
        # embedding_function=embed,
        embed,
        persist_directory=str(persist_dir),
    )
    vectordb.persist()
    print("[ingest] Ingestion complete.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf_dir", required=False, help="PDF directory (optional)")
    parser.add_argument("--persist_dir", required=False, help="Chroma persist dir (optional)")
    args = parser.parse_args()
    main(args.pdf_dir, args.persist_dir)

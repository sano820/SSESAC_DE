# utils.py

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.text_splitter import CharacterTextSplitter
from langchain_community.schema import Document
from typing import List
from pathlib import Path


def load_pdfs_from_directory(pdf_dir: Path) -> List[Document]:
    """Load all PDFs from `pdf_dir` and return a list of page-level Documents.

    Each Document.metadata contains a 'source' key (filename) to track origin.
    """
    docs: List[Document] = []
    pdf_paths = sorted([p for p in pdf_dir.glob("**/*.pdf") if p.suffix.lower() == ".pdf"])

    for p in pdf_paths:
        loader = PyPDFLoader(str(p))
        pages = loader.load_and_split()
        for pg in pages:
            meta = dict(pg.metadata) if pg.metadata else {}
            meta.setdefault("source", str(p.name))
            docs.append(Document(page_content=pg.page_content, metadata=meta))

    return docs


def split_docs(documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """Split Documents into chunks using CharacterTextSplitter and return new Documents with chunk metadata."""
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )

    all_chunks: List[Document] = []
    for d in documents:
        chunks = splitter.split_text(d.page_content)
        for i, c in enumerate(chunks):
            meta = dict(d.metadata) if d.metadata else {}
            meta["chunk"] = i
            all_chunks.append(Document(page_content=c, metadata=meta))

    return all_chunks

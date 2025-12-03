# utils.py
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.text_splitter import CharacterTextSplitter
from langchain_community.schema import Document
from typing import List
from pathlib import Path



def load_pdfs_from_directory(pdf_dir: Path) -> List[Document]:
    """주어진 디렉토리의 모든 PDF를 불러와서 페이지 단위 Document 리스트로 반환합니다.

    반환되는 Document의 metadata에는 'source' 키가 포함되어 원본 파일명을 추적합니다.
    """
    docs = []
    # PDF 파일 경로를 찾습니다.
    pdf_paths = sorted([p for p in pdf_dir.glob("**/*.pdf")])
    
    for p in pdf_paths:
        # 이 부분이 for p in pdf_paths: 블록 내부에 있도록 들여쓰기를 수정했습니다.
        loader = PyPDFLoader(str(p)) 
        
        # load_and_split을 사용하여 페이지 단위로 문서를 로드합니다.
        pages = loader.load_and_split()
        
        for pg in pages:
            # metadata 설정 (source filename 추적)
            meta = dict(pg.metadata) if pg.metadata else {}
            meta.setdefault("source", str(p.name))
            doc = Document(page_content=pg.page_content, metadata=meta)
            docs.append(doc)
            
    return docs


def split_docs(documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """문서들을 적절한 길이로 분할합니다. CharacterTextSplitter 사용."""
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    all_chunks = []
    for d in documents:
        # Document 객체 대신 페이지 내용을 분할합니다.
        chunks = splitter.split_text(d.page_content)
        for i, c in enumerate(chunks):
            meta = dict(d.metadata) if d.metadata else {}
            meta["chunk"] = i
            all_chunks.append(Document(page_content=c, metadata=meta))
    return all_chunks

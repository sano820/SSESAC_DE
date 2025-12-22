from __future__ import annotations

from typing import List, Dict, Any

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings

from src.config import Settings
from src.prompts import PROMPT


def _format_context(docs: List[Document]) -> str:
    # LLM이 출처를 쉽게 쓰도록 context에 메타 포함
    blocks = []
    for d in docs:
        src = d.metadata.get("source", "unknown")
        page = d.metadata.get("page", None)
        page_str = f"p.{page + 1}" if isinstance(page, int) else "p.?"
        blocks.append(f"[SOURCE: {src} | {page_str}]\n{d.page_content}")
    return "\n\n---\n\n".join(blocks)


def _extract_citations(docs: List[Document]) -> List[str]:
    seen = set()
    cites = []
    for d in docs:
        src = d.metadata.get("source", "unknown")
        page = d.metadata.get("page", None)
        page_str = f"{page + 1}" if isinstance(page, int) else "?"
        key = (src, page_str)
        if key not in seen:
            seen.add(key)
            cites.append(f"- {src} (p.{page_str})")
    return cites[:8]


def get_vectorstore(settings: Settings, collection_name: str = "ku_sejong_admissions") -> Chroma:
    embeddings = OllamaEmbeddings(
        model=settings.embed_model,
        base_url=settings.ollama_base_url,
    )
    return Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=settings.chroma_persist_dir,
    )


def build_rag_chain(settings: Settings):
    vs = get_vectorstore(settings)
    retriever = vs.as_retriever(search_kwargs={"k": 5})

    llm = ChatOllama(
        model=settings.chat_model,
        base_url=settings.ollama_base_url,
        temperature=0.2,
        # validate_model_on_init=True,  # 필요하면 켜기(모델 미다운로드 시 에러)
    )

    def with_retrieved_docs(inputs: Dict[str, Any]) -> Dict[str, Any]:
        question = inputs["question"]
        docs = retriever.invoke(question)
        inputs["docs"] = docs
        inputs["context"] = _format_context(docs)
        inputs["citations"] = _extract_citations(docs)
        return inputs

    chain = (
        RunnablePassthrough()
        | RunnableLambda(with_retrieved_docs)
        | PROMPT
        | llm
        | StrOutputParser()
    )
    return chain


def answer_question(question: str, profile: str, settings: Settings) -> Dict[str, Any]:
    chain = build_rag_chain(settings)
    result_text = chain.invoke({"question": question, "profile": profile})

    # retriever 결과 citations는 chain 내부에서 만들지만, 밖에서 다시 계산하려면 구조 변경 필요.
    # MVP로는 "출처는 LLM이 답변에 포함" + 아래는 안전장치로 문구 추가.
    return {
        "answer": result_text.strip(),
    }

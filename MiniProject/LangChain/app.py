import streamlit as st
from pathlib import Path
import config

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama

st.set_page_config(page_title="PDF RAG Chatbot (Local LLM - Ollama)", layout="wide")
st.title("📚 PDF RAG Chatbot — Streamlit + LangChain + Ollama (Local PDFs Only)")

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "retriever" not in st.session_state:
    st.session_state.retriever = None

# Sidebar
with st.sidebar:
    st.header("📁 로컬 PDF 기반 RAG 설정")

    persist_dir = st.text_input("Chroma Vector DB 경로", str(config.CHROMA_PERSIST_DIR))

    st.info(f"📂 로컬 PDF 디렉터리 사용 중:\n{config.PDF_DIR}")

    if st.button("📥 Ingestion 실행 (로컬 PDF → 벡터DB)"):
        from ingest import main as ingest_main
        try:
            ingest_main(str(config.PDF_DIR), persist_dir)
            st.success("Ingestion 완료! 이제 Vector DB 로드하세요.")
        except Exception as e:
            st.error(f"Ingestion 실패: {e}")

    if st.button("📦 Load Vector DB"):
        try:
            embed = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)
            vectordb = Chroma(persist_directory=str(persist_dir), embedding_function=embed)
            st.session_state.retriever = vectordb.as_retriever(search_kwargs={"k": config.RETRIEVER_TOP_K})
            st.success("Vector DB 로드 완료!")
        except Exception as e:
            st.error(f"DB 로드 실패: {e}")

    st.markdown("---")
    st.header("🤖 LLM 설정 (Ollama)")
    llm_model = st.text_input("Ollama 모델 이름", config.DEFAULT_OLLAMA_MODEL)
    temp = st.slider("Temperature", 0.0, 1.0, 0.2)

# Main UI
if st.session_state.retriever is None:
    st.info("🔍 먼저 로컬 PDF로 Ingestion 후, Vector DB를 Load 해주세요.")
else:
    llm = ChatOllama(model=llm_model, temperature=temp)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that answers based on the uploaded local documents."),
        ("human", "{question}"),
        ("system", "Retrieved context:\n{context}")
    ])

    # LCEL RAG chain: provide retriever as context
    rag_chain = (
        {"context": st.session_state.retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
    )

    st.subheader("💬 질문하기")
    query = st.text_input("질문을 입력하세요:", key="query_input")

    if st.button("전송") and query:
        with st.spinner(f"로컬 LLM({llm_model})이 답변 생성 중..."):
            try:
                response = rag_chain.invoke(query)
                # response might be an object; extract text content if present
                text = getattr(response, "content", None) or str(response)
                st.session_state.chat_history.append((query, text))
            except Exception as e:
                st.error(f"LLM 호출 오류: {e}")

    st.markdown("---")
    st.subheader("🧾 대화 기록")
    for q, a in reversed(st.session_state.chat_history):
        st.write(f"**Q:** {q}")
        st.write(f"**A:** {a}")
        st.markdown("---")

    if st.button("🧹 대화 초기화"):
        st.session_state.chat_history = []
        st.success("대화를 초기화했습니다.")

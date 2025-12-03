# app.py — Streamlit + LangChain + Chroma + Ollama (Local LLM RAG Chatbot)
# Streamlit + LangChain + Chroma + Ollama (Local LLM RAG Chatbot)

import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chains.retrieval import ConversationalRetrievalChain
from langchain_ollama import ChatOllama # Ollama 연동을 위한 클래스
from pathlib import Path
import config # 설정 파일 로드

st.set_page_config(page_title="PDF RAG Chatbot (Local LLM - Ollama)", layout="wide")
st.title("📚 PDF RAG Chatbot — Streamlit + LangChain + Ollama")

# ===============================
# Session State 초기화
# ===============================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "retriever" not in st.session_state:
    st.session_state.retriever = None

# ===============================
# Sidebar UI
# ===============================
with st.sidebar:
    st.header("📁 데이터베이스 / 모델 설정")

    # 기본 경로가 표시되도록 설정
    persist_dir = st.text_input("Chroma Vector DB 경로", str(config.CHROMA_PERSIST_DIR))

    uploaded_files = st.file_uploader("PDF 파일 업로드", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        save_dir = Path(config.PDF_DIR)
        save_dir.mkdir(parents=True, exist_ok=True)
        for file in uploaded_files:
            file_path = save_dir / file.name
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
        st.success(f"📄 {len(uploaded_files)}개 PDF 저장 완료 → {save_dir}")

    # Ingestion 버튼: ingest.py 실행
    if st.button("📥 Ingestion 실행 (PDF → 벡터DB)"):
        # 로드 성공 시에만 ingest.py import
        from ingest import main as ingest_main
        try:
            # Streamlit 환경에서 config.PDF_DIR에 저장된 PDF를 처리하도록 합니다.
            ingest_main(str(config.PDF_DIR), persist_dir) 
            st.success("Ingestion 완료! 이제 Load Vector DB 누르세요.")
        except Exception as e:
             st.error(f"Ingestion 실패: {e}. 'ingest.py'를 로컬에서 먼저 실행해보세요.")

    # Vector DB 로드 버튼
    if st.button("📦 Load Vector DB"):
        try:
            # 임베딩 모델 로드
            embed = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)
            # Chroma DB 로드
            vectordb = Chroma(persist_directory=str(persist_dir), embedding_function=embed)
            # 리트리버 설정
            st.session_state.retriever = vectordb.as_retriever(search_kwargs={"k": config.RETRIEVER_TOP_K})
            st.success("Vector DB 로드 완료!")
        except Exception as e:
            st.error(f"DB 로드 실패: {e}")

    st.markdown("---")
    st.header("🤖 LLM 설정 (Ollama)")
    # Ollama 모델 이름 설정 (로컬에 pull 되어 있어야 합니다)
    llm_model = st.text_input("Ollama 모델 이름", config.DEFAULT_OLLAMA_MODEL)
    temp = st.slider("Temperature", 0.0, 1.0, 0.2)

# ===============================
# Main Chat UI
# ===============================
if st.session_state.retriever is None:
    st.info("🔍 먼저 PDF 파일을 업로드/Ingest 후, Vector DB를 Load 해주세요.")
else:
    # Ollama LLM 인스턴스 생성
    llm = ChatOllama(model=llm_model, temperature=temp)
    # ConversationalRetrievalChain 설정
    qa_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=st.session_state.retriever)

    st.subheader("💬 질문하기")
    query = st.text_input("질문을 입력하세요:", key="query_input")

    # 질문 전송 및 답변 생성
    if st.button("전송") and query:
        with st.spinner(f"로컬 LLM ({llm_model})이 답변 생성 중..."):
            try:
                # qa_chain 호출
                result = qa_chain.invoke({"question": query, "chat_history": st.session_state.chat_history})
                answer = result.get("answer", "(응답 없음)")
                # 대화 기록 업데이트
                st.session_state.chat_history.append((query, answer))
            except Exception as e:
                st.error(f"LLM 호출 오류: {e}. Ollama 서버가 실행 중인지 확인하고, 모델({llm_model})이 설치되어 있는지 'ollama list'로 확인해 보세요.")


    st.markdown("---")
    st.subheader("🧾 대화 기록")
    # 대화 기록을 최신순으로 표시
    for q, a in reversed(st.session_state.chat_history):
        st.write(f"**Q:** {q}")
        st.write(f"**A:** {a}")
        st.markdown("---")

    if st.button("🧹 대화 초기화"):
        st.session_state.chat_history = []
        st.success("대화를 초기화했습니다.")
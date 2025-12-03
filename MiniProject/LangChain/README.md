# 📚 Streamlit 기반 로컬 RAG 챗봇 (Ollama + ChromaDB)
이 프로젝트는 Streamlit을 사용하여 사용자 친화적인 웹 인터페이스를 제공하며, 로컬 LLM 환경(Ollama), Chroma 벡터 데이터베이스, 그리고 Hugging Face 임베딩을 결합한 Retrieval-Augmented Generation (RAG) 챗봇입니다. 로컬 PDF 문서들을 데이터베이스화하여 질문에 대한 답변을 생성할 수 있습니다.

## ✨ 주요 특징로컬 
- LLM 지원: Ollama를 사용하여 로컬에서 LLM을 실행하고 연동합니다.문서 기반 질의응답 (RAG): 사용자가 업로드한 PDF 파일에서 관련 정보를 검색하여 답변의 정확도를 높입니다.
- Streamlit UI: 간편하게 사용할 수 있는 웹 인터페이스를 제공합니다.ChromaDB: 로컬에서 문서를 임베딩하고 저장하기 위한 벡터 데이터베이스를 사용합니다.
- 최신 LangChain 호환: langchain-community 패키지를 활용하여 최신 LangChain 1.x 버전 환경과 호환되도록 구성되었습니다.

## ⚙️ 필수 구성 요소
프로젝트를 실행하기 위해 다음 환경이 필요합니다.
- Python 3.x (가상 환경 권장)
- Ollama: 로컬 LLM 서버 (LLM 모델 설치 필요, 예: llama3)  

Ollama 서버 설정
- Ollama가 설치되어 있고, 사용할 모델이 로컬에 다운로드되어 있어야 합니다.

## 📝 사용 방법

1. PDF 문서 준비  

질의응답에 사용하고자 하는 PDF 파일들을 config.py에서 지정한 경로(pdfs/ 폴더)에 저장합니다.

2. Ingestion (벡터 DB 구축)

PDF 문서를 읽고 청크 단위로 분할한 후, 임베딩을 생성하여 ChromaDB에 저장하는 과정입니다.
```
A. 콘솔에서 실행 (권장)

python ingest.py
# (옵션: 특정 경로 지정 시)
# python ingest.py --pdf_dir ./my_pdfs --persist_dir ./my_db
```
```
B. Streamlit 앱에서 실행

Streamlit 앱을 실행한 후, 사이드바의 "📥 Ingestion 실행" 버튼을 눌러 실행할 수 있습니다.
```
3. Streamlit 앱 실행

벡터 DB 구축이 완료되면, Streamlit 애플리케이션을 실행합니다.
```
streamlit run app.py
```

4. 챗봇 사용

웹 페이지가 열리면, 사이드바에서 "📦 Load Vector DB" 버튼을 클릭하여 Chroma DB를 메모리에 로드합니다.

하단 채팅창에 질문을 입력하고 "전송" 버튼을 눌러 RAG 기반 답변을 받습니다.
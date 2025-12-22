import streamlit as st

from src.config import get_settings
from src.rag import answer_question
from src.rules import UserProfile, load_rules, recommend_six


st.set_page_config(page_title="KU Sejong Admissions Bot", layout="wide")
settings = get_settings()

st.title("고려대학교 세종캠퍼스 입시 컨설팅 챗봇 (RAG + Ollama)")
st.caption("※ 답변은 업로드한 요강/시행계획 문서를 근거로 하며, 출처(문서/페이지)를 포함합니다.")


with st.sidebar:
    st.header("사용자 프로필")
    track = st.selectbox("전형 트랙", ["수시", "정시"])
    major_keyword = st.text_input("희망 학과 키워드", value="컴퓨터")
    preference = st.selectbox("선호", ["안전 위주", "적정 위주", "상향 도전"])

    gpa = None
    csat_summary = None

    if track == "수시":
        gpa = st.number_input("내신(예: 2.3)", min_value=1.0, max_value=9.0, value=2.5, step=0.1)
    else:
        csat_summary = st.text_input("수능/모의고사 요약(예: 국2 수2 영2 탐2/3)", value="국2 수2 영2 탐2/3")

    profile = UserProfile(
        track=track,
        gpa=float(gpa) if gpa is not None else None,
        csat_summary=csat_summary,
        major_keyword=major_keyword,
        preference=preference,
    )

    st.divider()
    st.subheader("추천(6개 조합)")
    do_reco = st.button("6개 조합 추천 보기")


col_chat, col_cards = st.columns([2, 1])

with col_cards:
    st.subheader("추천 카드")
    if do_reco:
        rules = load_rules()
        recos = recommend_six(profile, rules)
        if not recos:
            st.warning("아직 rules_ku_sejong_2026.json이 비어있어요. (MVP에서는 수동으로 6개 후보부터 넣어도 OK)")
        else:
            for r in recos:
                st.markdown(f"**[{r['bucket']}] {r['program']} / {r['track']}**")
                st.write(r["note"])
                st.divider()
    else:
        st.info("좌측에서 버튼을 누르면 6개 조합 카드가 표시됩니다.")


with col_chat:
    st.subheader("채팅")
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "안녕하세요! 고려대 세종캠퍼스 모집요강 기반으로 답변해드릴게요. 질문을 입력해 주세요."}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_question = st.chat_input("예: 세종캠 수시 학생부교과 전형 수능최저 있어?")
    if user_question:
        st.session_state.messages.append({"role": "user", "content": user_question})
        with st.chat_message("user"):
            st.write(user_question)

        profile_text = f"- 트랙: {profile.track}\n- 희망: {profile.major_keyword}\n- 선호: {profile.preference}\n"
        if profile.gpa is not None:
            profile_text += f"- 내신: {profile.gpa}\n"
        if profile.csat_summary:
            profile_text += f"- 수능요약: {profile.csat_summary}\n"

        with st.chat_message("assistant"):
            with st.spinner("문서 검색 + 답변 생성 중..."):
                result = answer_question(user_question, profile_text, settings)
                st.write(result["answer"])

        st.session_state.messages.append({"role": "assistant", "content": result["answer"]})

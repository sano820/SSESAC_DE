import module as oam
from dotenv import load_dotenv

load_dotenv()
oam.test_openai()

print("\n=== Response 값 반환 ===")
response = oam.respon(input="오늘 서울 날씨 알려줘")
print(response)

print("\n=== Respnse Content 값 반환 ===")
content = oam.check_content(response)
print(content)

initial_input ="""
나는 여름 휴가를 계획 중이야. 따뜻한 날씨를 좋아하고, 자연 경관과 역사적인 장소를 둘러보는 걸 좋아해.
어떤 여행지가 나에게 적합할까?
"""
prompt_chain = [
    ## 여행 후보지 3곳을 추천하고 그 이유를 설명
"""사용자의 여행 취향을 바탕으로 적합한 여행지 3곳을 추천하세요.
먼저 사용자가 입력한 희망사항을 요약해줘
사용자가 입력한 희망사항을 반영해서 왜 적합한 여행지인지 설명해주세요
각 여행지의 기후, 주요 관광지, 활동 등을 설명하세요.
""",

    ## 여행지 1곳을 선택하고 활동 5가지 나열
"""다음 여행지 3곳 중 하나를 선택하세요. 선택한 여행지 알려주세요. 그리고 선택한 이유를 설명해주세요.
해당 여행지에서 즐길 수 있는 주요 활동 5가지를 나열하세요.
활동은 자연 탐방, 역사 탐방, 음식 체험 등 다양한 범주에서 포함되도록 하세요.
""",

    ## 선택한 여행지에서 하루 일정 계획
"""사용자가 하루 동안 이 여행지에서 시간을 보낼 계획입니다.
오전, 오후, 저녁으로 나누어 일정을 짜고, 각 시간대에 어떤 활동을 하면 좋을지 설명하세요.
"""
]
responses = oam.prompt_chain_workflow_2(initial_input, prompt_chain)
final_answer = responses[-1]
print("\n===비동기 작업 실습하기===\n",final_answer)


# --- 라우팅
query1 = '리스본 여행 일정 짜줘'
response = oam.run_router_workflow(query1)
print("\n===라우팅 실습하기===\n",response)
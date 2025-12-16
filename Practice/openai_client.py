# openai_client.py
import module as oam
from prompts.travel_chain import initial_input, prompt_chain
from dotenv import load_dotenv

load_dotenv()
oam.test_openai()

print("\n=== Response 값 반환 ===")
response = oam.respon(input="오늘 서울 날씨 알려줘")
print(response)

print("\n=== Respnse Content 값 반환 ===")
content = oam.check_content(response)
print(content)


responses = oam.prompt_chain_workflow_2(initial_input, prompt_chain)
final_answer = responses[-1]
print("\n===비동기 작업 실습하기===\n",final_answer)


# --- 라우팅
query1 = '리스본 여행 일정 짜줘'
response = oam.run_router_workflow(query1)
print("\n===라우팅 실습하기===\n",response)
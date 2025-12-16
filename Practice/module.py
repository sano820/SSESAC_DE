# module.py
from functools import lru_cache

from typing import List, Optional, Dict
from openai import OpenAI
from langchain_openai import ChatOpenAI

#------ 객체 생성 한번하기
@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    # OpenAI()는 프로그램 전체에서 딱 1번만 생성되어 재사용됨
    return OpenAI()

#-----------1215

def test_openai():
    model = ChatOpenAI(model = 'gpt-4o', temperature=0)
    ai_message = model.invoke("안녕하세요.")
    print(ai_message)

def respon(input = False):
    message =[{'role':'system', 'content':'You are a 10years developer of AI'},{ 'role':'user', 'content':input}]
    client = OpenAI()
    response = client.chat.completions.create(model = 'gpt-4o', messages= message)
    return response

def check_content(response) -> str:
    content = response.choices[0].message.content
    return content



# -------------1216



def llm_call(prompt: str, model: str = 'gpt-4o-mini') -> str:
    sync_client = OpenAI()
    messages = []
    messages.append({'role':'user','content':prompt})
    chat_completion = sync_client.chat.completions.create(
        model = model,
        messages=messages
    )
    return chat_completion.choices[0].message.content

def prompt_chain_workflow_2(initial_input:str, prompt_chain:List[str]) -> List[str]:
    response_chain = []
    response = initial_input
    for i, prompt in enumerate(prompt_chain, 1):
        print(f"\n == 단계 {i} == \n")
        final_prompt = f'{prompt} \n\n 문맥(Context):\n {response} \n 사용자 입력 : {initial_input}'
        print(f' 프롬프트 : \n {final_prompt} \n')
        response = llm_call(final_prompt)
        response_chain.append(response)
    return response_chain

def run_router_workflow(user_prompt:str):
    router_prompt = f"""
    사용자의 프롬프트/질문: {user_prompt}

    각 모델은 서로 다른 기능을 가지고 있습니다. 사용자의 질문에 가장 적합한 모델을 선택하세요:
    
    gpt-4o: 일반적인 작업에 가장 적합한 모델 (기본값)
    gpt-5.2-thinking: 코딩 및 복잡한 문제 해결에 적합한 모델
    gpt-4o-mini: 간단한 사칙연산 등의 작업에 적합한 모델

    모델명만 단답형으로 응답하세요
    """
    selected_model = llm_call(router_prompt)
    response = llm_call(user_prompt, model = selected_model)
    return response


# ---------- 비동기 + 라우터
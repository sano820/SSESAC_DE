from langchain_openai import ChatOpenAI
from openai import OpenAI
def test_openai():
    model = ChatOpenAI(model = 'gpt-4o', temperature=0)
    ai_message = model.invoke("안녕하세요.")
    print(ai_message)

def respon(input = False):
    message =[{'role':'system', 'content':'You are a 10years developer of AI', 'role':'user', 'content':input}]
    client = OpenAI()
    response = client.chat.completions.create(model = 'gpt-4o', messages= message)
    return dict(response)

def check_content(response):
    content = response["choices"][0].message.content
    return content


from langchain_openai import ChatOpenAI

def test_openai():
    model = ChatOpenAI(model = 'gpt-4o', temperature=0)
    ai_message = model.invoke("안녕하세요.")
    print(ai_message)
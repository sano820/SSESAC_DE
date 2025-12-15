import module as oam
from dotenv import load_dotenv

load_dotenv()
oam.test_openai()

print("===")
response = oam.respon(input="오늘 서울 날씨 알려줘")
print(response)

print("===")
content = oam.check_content(response)
print(content)


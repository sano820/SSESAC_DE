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


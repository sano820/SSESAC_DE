from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys  

from bs4 import BeautifulSoup 
import json
import time


options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
driver.get("https://www.naver.com/")
time.sleep(1)

query = driver.find_element(By.ID, "query")
query.send_keys("서울 날씨")
time.sleep(1)

# 버튼 대신 엔터키를 입력하기
query.send_keys(Keys.ENTER)

# 3. 로딩 완료 대기
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "weather_info"))
    
)

# 4. 현재 페이지 HTML 가져오기 (Selenium -> BeautilfulSoup 전달)
html = driver.page_source
bs = BeautifulSoup(html, "html.parser")

weather_info = bs.select_one("div.status_wrap")

# 현재 온도
tem_today = weather_info.select_one("div._today strong").get_text(strip=True)

# 현재 날씨 상태
state_today = weather_info.select_one("div._today div.temperature_info span.weather").get_text(strip=True)


misae_rate = weather_info.select("ul.today_chart_list li.item_today")
misae = []
for rate in misae_rate:
    title = rate.select_one("strong.title").get_text()
    txt = rate.select_one("span.txt").get_text()
    misae.append((title, txt))

# 미세먼지 정도
rate_misae = misae[0][0]+' '+misae[0][1]
# 초 미세먼지 정도
rate_chomisae = misae[1][0]+' '+misae[1][1]

# 자외선 정도
jwhyline = misae[2][0]+' '+misae[2][1]


# 이미지 url은 하드코딩 하기
image_state = {
    "맑음" : 1,
    "맑음(밤)":2,
    "구름 조금":3,
    "구름 조금(밤)":4,
    "구름 많음" : 5,
    "구름 많음(밤)":6,
    "흐림" : 7,
    # 아래 링크 참고
    # https://help.naver.com/service/5600/contents/12371?osType=COMMONOS
    "구름 많고 한때 비" : 22
}
a = image_state["맑음"]
url = f"https://ssl.pstatic.net/sstatic/keypage/outside/scui/weather_new_new/img/weather_svg_v2/icon_flat_wt{a}.svg"

answer = [{
    "현재 온도" : tem_today[5:-1],
    "이미지 url" : url,
    "현재 날씨 상태" : state_today,
    "미세먼지 정도" : rate_misae,
    "초 미세먼지 정도" : rate_chomisae,
    "자외선 정도" : jwhyline
}]


with open("./1113/outputs/[mission2]answers.json", "w", encoding="utf-8") as f:
    json.dump(answer, f, ensure_ascii=False, indent=2)

driver.quit()
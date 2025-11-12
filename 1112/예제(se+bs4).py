from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys  

from bs4 import BeautifulSoup 
import time


# 1. 브라우저 실행
driver = webdriver.Chrome()
driver.get("https://quotes.toscrape.com/scroll")

# 2. 무한 스크롤 (Selenium 역할)
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1.5)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# 3. 로딩 완료 대기
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, "quote"))
    
)

# 4. 현재 페이지 HTML 가져오기 (Selenium -> BeautilfulSoup 전달)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# 5. BeautifulSoup으로 데이터 추출
quotes = soup.select(".quote")

for q in quotes[:5]:
    text = q.select_one(".text").get_text(strip=True)
    author = q.select_one(".author").get_text(strip=True)
    print(f"{text} - {author}")

driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys   # 버튼 대신에 엔터키 입력하기
import time


options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

url = "https://naver.com"
driver.get(url)
time.sleep(1)

query = driver.find_element(By.ID, "query")
query.send_keys("데이터 엔지니어링")
time.sleep(1)

# search_btn = driver.find_element(By.CSS_SELECTOR, "#search-btn")
# search_btn.click()

# 버튼 대신 엔터키를 입력하기
query.send_keys(Keys.ENTER)
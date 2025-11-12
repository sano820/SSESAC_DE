from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys   # 버튼 대신에 엔터키 입력하기
from dotenv import load_dotenv
import os, time

load_dotenv()
naver_id = os.getenv("naver_id")
naver_pw = os.getenv("naver_pw")


options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)

url = "https://naver.com"
driver.get(url)
time.sleep(1)

login_btn = driver.find_element(By.CSS_SELECTOR, "a.MyView-module__link_login___HpHMW")
login_btn.click()
time.sleep(1)

id_input = driver.find_element(By.ID, "id")
id_input.send_keys(naver_id)
time.sleep(1)

pw_input = driver.find_element(By.ID, "pw")
pw_input.send_keys(naver_pw)
time.sleep(1)

enter_btn = driver.find_element(By.ID, "log.login")
enter_btn.click()


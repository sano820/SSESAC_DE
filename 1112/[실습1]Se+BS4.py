from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys  

from bs4 import BeautifulSoup 
import json
import time


# 1. 브라우저 실행
driver = webdriver.Chrome()
driver.get("https://www.scrapethissite.com/pages/forms/?per_page=600")

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
    EC.presence_of_element_located((By.CLASS_NAME, "team"))
    
)

# 4. 현재 페이지 HTML 가져오기 (Selenium -> BeautilfulSoup 전달)
html = driver.page_source
bs = BeautifulSoup(html, "html.parser")

data = []

for item in bs.select("tr.team"):

        team_name = item.select_one("td.name").get_text(strip=True)
        year = item.select_one("td.year").get_text(strip=True)
        wins = item.select_one("td.wins").get_text(strip=True)
        loss = item.select_one("td.losses").get_text(strip=True)
        OT_loss = item.select_one("td.ot-losses").get_text(strip=True)
        gf = item.select_one("td.gf").get_text(strip=True)
        ga = item.select_one("td.ga").get_text(strip=True)


        # # 기준 값 조건
        # win_p = item.select_one("td.pct").get_text(strip=True)
        # if float(win_p) >=0.5:
        #     p_win = win_p+'(success)'
        # else:
        #     p_win = win_p+'(danger)'

        # tag 속성 값으로 수정
        win_p = item.select_one("td.pct")
        if "text-success" in win_p["class"]:
            p_win = win_p.get_text(strip=True) + '(success)'
        elif "text-danger" in win_p["class"]:
            p_win = win_p.get_text(strip=True) + '(danger)'


        # # 기준 값 조건
        # rg  = item.select_one("td.diff").get_text(strip=True)
        # if float(rg) >= 0:
        #     success = rg + '(success)'
        # else:
        #     success = rg + '(danger)'

        # tag 속성 값으로 수정
        rg = item.select_one("td.diff")
        if "text-success" in rg["class"]:
            success = rg.get_text(strip=True) + '(success)'
        elif "text-danger" in win_p["class"]:
            success = rg.get_text(strip=True) + '(danger)'
        
        data.append({
                "Team Name": team_name,
                "Year":year,
                "Wins" : wins,
                "Losses": loss,
                "OT Losses":OT_loss,
                "win":p_win,
                "Goals For(GF)":gf,
                "Goals Against(GA)":ga,
                "+ / -" : success
        })
        print(f"Team Name:{team_name}, Year : {year}, Wins : {wins}, Losses:{loss}, OT Losses:{OT_loss}, win %:{p_win}, Goals For(GF) : {gf}, Goals Against(GA) : ga, +/- : {success}")

with open("./1112/outputs/sebs4_answers.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

driver.quit()
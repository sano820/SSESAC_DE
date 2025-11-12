import requests 
from bs4 import BeautifulSoup 
import json
import pandas as pd



data = []
for page in range(1, 7):
    url = f"https://www.scrapethissite.com/pages/forms/?page_num={page}&per_page=100" 
    res = requests.get(url)   
    bs = BeautifulSoup(res.text, "html.parser")



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

with open("./1112/outputs/bs4_answers_tag.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

df = pd.DataFrame(data)
df.to_csv(f"./1112/outputs/bs4_answers_tag.csv", index=False, encoding="utf-8")

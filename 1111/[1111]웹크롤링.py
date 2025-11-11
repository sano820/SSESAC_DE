import requests 
from bs4 import BeautifulSoup 
import pandas as pd

url = "https://www.scrapethissite.com/pages/simple/" 
res = requests.get(url)   
bs = BeautifulSoup(res.text)

# # 크롤링 되었는지 확인
# print(bs)
# # 모든 나라의 이름 가져오기
# print(bs.select("h3.country-name"))
# # andorra만 가져오기
# print(bs.select_one("h3.country-name"))
# # andorra 이름만 가져오기
# andorra = bs.select_one("h3.country-name")
# print(andorra.get_text(strip = True))

# andorra와 관련된 모든 내용 가져오기~
countries = bs.select_one("div.row div.col-md-4.country")
# print(contries)

# 나라가 여러개 이므로 for문과 함게 활용
# for row in bs.select("div.row div.col-md-4.country"):
#     print(row)

data = []
# 반복적으로 나라 정보 수집 후 출력
for country in bs.select("div.row div.col-md-4.country"):

    name = country.select_one("h3.country-name").get_text(strip=True)

    info = country.select_one("div.country-info")
    capital = info.select_one("span.country-capital").get_text(strip=True)
    population = info.select_one("span.country-population").get_text(strip=True)
    area = info.select_one("span.country-area").get_text(strip=True)

    data.append({
        "name":name,
        "capital": capital,
        "population":population,
        "area":area
    })
    print(f"name:{name}, capital:{capital}, population:{population}, area:{area}")

df = pd.DataFrame(data)
df.to_csv("./1111/countries.csv", index = False, encoding = "utf-8")
import requests 
from bs4 import BeautifulSoup 
import json
import pandas as pd

sites =[["laptops",21], ["tablets", 5], ["touch", 3]]

data = []
for site in sites:
    for page in range(1, site[1]):
        url = f"https://webscraper.io/test-sites/e-commerce/static/computers/{site[0]}?page={page}" 
        res = requests.get(url)   
        bs = BeautifulSoup(res.text, "html.parser")



        for item in bs.select("div.card.thumbnail div.product-wrapper.card-body"):

            image_tag = item.select_one("img.img-fluid.card-img-top.image.img-responsive")
            image_link = image_tag["src"]

            caption = item.select_one("div.caption")
            price = caption.select_one("h4.price.float-end.card-title.pull-right span").get_text(strip=True)
            name = caption.select_one("h4 a.title").get_text(strip=True)
            link = caption.select_one("h4 a.title")
            info_link = link['href']
            info = caption.select_one("p.description.card-text").get_text(strip=True)

            rating = item.select_one("div.ratings")
            review_count = rating.select_one("p.review-count.float-end span").get_text(strip=True)
            star_tag = rating.select_one("p:nth-of-type(2)")
            star_count = star_tag['data-rating']
            

            data.append({
                "카테 고리":site[0],
                "사진의 주소 URL":image_link,
                "상품 이름" : name,
                "가격": price,
                "상세 스펙 텍스트":info,
                "상세 페이지":info_link,
                "리뷰 개수":review_count,
                "별의 개수":star_count
            })
            print(f"il:{image_link}, name : {name}, info : {info}, price:{price}, review_count:{review_count}, star_count:{star_count}")

with open("./1111/outputs/all_products.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

df = pd.DataFrame(data)
df.to_csv(f"./1111/outputs/all_rpducts.csv", index=False, encoding="utf-8")
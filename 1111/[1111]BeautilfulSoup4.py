import requests 
from bs4 import BeautifulSoup 
import pandas as pd

data_laptops = []

for page in range(1, 21):
    url = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops?page={page}" 
    res = requests.get(url)   
    bs = BeautifulSoup(res.text)



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
        

        data_laptops.append({
            "사진의 주소 URL":image_link,
            "상품 이름" : name,
            "가격": price,
            "상세 스펙 텍스트":info,
            "상세 페이지":info_link,
            "리뷰 개수":review_count,
            "별의 개수":star_count
        })
        print(f"il:{image_link}, name : {name}, info : {info}, price:{price}, review_count:{review_count}, star_count:{star_count}")

df_laptops = pd.DataFrame(data_laptops)
df_laptops.to_csv("./1111/outputs/laptops.csv", index = False, encoding = "utf-8")


data_tablets = []

for page in range(1, 5):
    url = "https://webscraper.io/test-sites/e-commerce/static/computers/tablets?page={page}" 
    res = requests.get(url)   
    bs = BeautifulSoup(res.text)



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
        

        data_tablets.append({
            "사진의 주소 URL":image_link,
            "상품 이름" : name,
            "가격": price,
            "상세 스펙 텍스트":info,
            "상세 페이지":info_link,
            "리뷰 개수":review_count,
            "별의 개수":star_count
        })
        print(f"il:{image_link}, name : {name}, info : {info}, price:{price}, review_count:{review_count}, star_count:{star_count}")

df_tablets = pd.DataFrame(data_tablets)
df_tablets.to_csv("./1111/outputs/tablets.csv", index = False, encoding = "utf-8")




data_toches = []

for page in range(1, 3):
    url = "https://webscraper.io/test-sites/e-commerce/static/phones/touch?page={page}" 
    res = requests.get(url)   
    bs = BeautifulSoup(res.text)



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
        

        data_toches.append({
            "사진의 주소 URL":image_link,
            "상품 이름" : name,
            "가격": price,
            "상세 스펙 텍스트":info,
            "상세 페이지":info_link,
            "리뷰 개수":review_count,
            "별의 개수":star_count
        })
        print(f"il:{image_link}, name : {name}, info : {info}, price:{price}, review_count:{review_count}, star_count:{star_count}")

df_toches = pd.DataFrame(data_toches)
df_toches.to_csv("./1111/outputs/toches.csv", index = False, encoding = "utf-8")
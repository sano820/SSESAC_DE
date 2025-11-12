import requests 
from bs4 import BeautifulSoup 
import json
import pandas as pd

categories = [
    ["travel_2",1],
    ["mystery_3",2],
    ["historical-fiction_4",2],
    ["sequential-art_5",4],
    ["classics_6",1],
    ["philosophy_7",1],
    ["romance_8",2],
    ["womens-fiction_9",1],
    ["fiction_10",4],
    ["childrens_11",2],
    ["religion_12",1],
    ["nonfiction_13",6],
    ["music_14",1],
    ["default_15",8],
    ["science-fiction_16",1],
    ["sports-and-games_17",1],
    ["add-a-comment_18",4],
    ["fantasy_19",3],
    ["new-adult_20",1],
    ["young-adult_21",3],
    ["science_22",1],
    ["poetry_23",1],
    ["paranormal_24",1],
    ["art_25",1],
    ["psychology_26",7],
    ["autobiography_27",1],
    ["parenting_28",1],
    ["adult-fiction_29",1],
    ["humor_30",1],
    ["horror_31",1],
    ["history_32",1],
    ["food-and-drink_33",2],
    ["christian-fiction_34",1],
    ["business_35",1],
    ["biography_36",1],
    ["thriller_37",1],
    ["contemporary_38",1],
    ["spirituality_39",1],
    ["academic_40",1],
    ["self-help_41",1],
    ["historical_42",1],
    ["christian_43",1],
    ["suspense_44",1],
    ["short-stories_45",1],
   ["novels_46",1],
    ["health_47",1],
    ["politics_48",1],
    ["cultural_49",1],
    ["erotica_50",1],
    ["crime_51",1]
]

answer = []
for c in categories:
    url = f"https://books.toscrape.com/catalogue/category/books/{c[0]}/index.html"
    res_or = requests.get(url)   
    bs_or = BeautifulSoup(res_or.text, "html.parser")

    pages = c[1]
    items = []
    if pages == 1:
        p = 1
        url = f"https://books.toscrape.com/catalogue/category/books/{c[0]}/index.html"
        res = requests.get(url)   
        bs = BeautifulSoup(res.text, "html.parser")

        data = []
        for item in bs.select("li.col-xs-6.col-sm-4.col-md-3.col-lg-3"):

            image_url = item.select_one("div.image_container img.thumbnail")["src"]
            info_url = item.select_one("div.image_container a")["href"]
            stars = item.select_one("p.star-rating")["class"]
            title = item.select_one("h3 a").get_text(strip=True)
            price = item.select_one("div.product_price p.price_color").get_text(strip=True)


                    
            data.append({
                    "title": title,
                    "price":price,
                    "stars" : stars[1],
                    "image_url": image_url,
                    "detail_url":info_url
            })
        items.append({
                "page" : p,
                "data" : data
        })
    elif pages > 1:
        for p in range(1, c[1]+1):
            url = f"https://books.toscrape.com/catalogue/category/books/{c[0]}/page-{p}.html"
            res = requests.get(url)   
            bs = BeautifulSoup(res.text, "html.parser")

            data = []
            for item in bs.select("li.col-xs-6.col-sm-4.col-md-3.col-lg-3"):

                image_url = item.select_one("div.image_container img.thumbnail")["src"]
                info_url = item.select_one("div.image_container a")["href"]
                stars = item.select_one("p.star-rating")["class"]
                title = item.select_one("h3 a").get_text(strip=True)
                price = item.select_one("div.product_price p.price_color").get_text(strip=True)


                    
                data.append({
                        "title": title,
                        "price":price,
                        "stars" : stars[1],
                        "image_url": image_url,
                        "detail_url":info_url
                })
            
            items.append({
                "page" : p,
                "data" : data
            })
    answer.append({
        "genre": c[0],
        "items":items
    })


with open("./1112/outputs/[mission2]answers.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# df = pd.DataFrame(data)
# df.to_csv(f"./1112/outputs/bs4_answers_tag.csv", index=False, encoding="utf-8")


import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from urllib.parse import urljoin

client = MongoClient("localhost", 27017)
db = client.jungle

url = "https://books.toscrape.com/"

data = requests.get(url)
data.encoding = "utf-8"

soup = BeautifulSoup(data.text, "html.parser")

books = soup.select("article.product_pod")

# 중복 저장 방지: 실행할 때마다 기존 books 데이터 삭제
db.books.delete_many({})

for book in books:
    title = book.select_one("h3 > a")["title"]
    price = book.select_one(".price_color").text
    stock = book.select_one(".availability").text.strip()

    rating_tag = book.select_one(".star-rating")
    rating = rating_tag["class"][1]

    link = book.select_one("h3 > a")["href"]
    full_link = urljoin(url, link)

    doc = {
        "title": title,
        "price": price,
        "stock": stock,
        "rating": rating,
        "link": full_link
    }

    db.books.insert_one(doc)

print("저장 완료")
print("저장 개수:", db.books.count_documents({}))
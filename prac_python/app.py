import requests
from bs4 import BeautifulSoup

data = requests.get("https://books.toscrape.com/")
data.encoding = "utf-8"

soup = BeautifulSoup(data.text, "html.parser")

books = soup.select("article.product_pod")

print("--------------------------------")
print("책 개수:", len(books))
print("--------------------------------")

for book in books:
    title = book.select_one("h3 > a")["title"]
    price = book.select_one(".price_color").text
    stock = book.select_one(".availability").text.strip()

    print(title, price, stock)
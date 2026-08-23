import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

data = requests.get('https://books.toscrape.com/', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

books = soup.select('article.product_pod')

for book in books:
    title = book.select_one('h3 a')['title']

    price = book.select_one('.price_color').text
    stock = book.select_one('.instock.availability').text.strip()

    rating_element = book.select_one('.star-rating')
    rating = rating_element['class'][1]

    print(title, price, stock, rating)
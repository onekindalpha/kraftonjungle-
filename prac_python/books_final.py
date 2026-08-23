import requests

from bs4 import BeautifulSoup
from pymongo import MongoClient
from urllib.parse import urljoin

client = MongoClient('localhost', 27017)
db = client.jungle_practice_safe


def insert_all():
    # URL을 읽어서 HTML을 받아오고
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }

    url = 'https://books.toscrape.com/'
    data = requests.get(url, headers=headers)
    data.encoding = "utf-8"

    # HTML을 BeautifulSoup으로 검색하기 쉽게 만듦
    soup = BeautifulSoup(data.text, 'html.parser')

    # 책 하나하나를 불러오기
    books = soup.select('article.product_pod')
    print("가져온 책 개수:", len(books))

    # books 반복문 돌리기
    for book in books:
        # 책 제목이 들어있는 a 태그 가져오기
        tag_element = book.select_one('h3 > a')
        if not tag_element:
            continue

        # 책 제목 가져오기
        title = tag_element['title']

        # 책 상세페이지 링크 가져오기
        link = tag_element['href']
        link = urljoin(url, link)

        # 가격 가져오기
        price = book.select_one(".price_color").text.strip()
        price = price.replace("£", "").replace("Â", "")
        price = float(price)

        # 재고 상태 가져오기
        stock = book.select_one('.instock.availability').text.strip()

        # 별점 가져오기
        rating_element = book.select_one('.star-rating')
        rating = rating_element['class'][1]

        # MongoDB에 넣을 데이터 만들기
        doc = {
            'title': title,
            'link': link,
            'price': price,
            'stock': stock,
            'rating': rating
        }

        # MongoDB에 저장
        db.books.insert_one(doc)

        print("완료", title, price, stock, rating)


if __name__ == '__main__':
    # 책 사이트를 scraping 해서 DB에 채우기
    insert_all()
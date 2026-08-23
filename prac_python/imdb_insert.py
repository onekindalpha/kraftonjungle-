import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.jungle  # DB 이름: jungle

def insert_all():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }

    data = requests.get(
        'https://www.imdb.com/chart/top/?ref_=nv_mv_250',
        headers=headers
    )

    print("status code:", data.status_code)
    print("html 길이:", len(data.text))

    soup = BeautifulSoup(data.text, 'html.parser')

    movies = soup.select('.ipc-metadata-list > li')
    print("영화 개수:", len(movies))

    for movie in movies:
        tag_element = movie.select_one('.ipc-title-link-wrapper > h3')
        if not tag_element:
            continue

        title = tag_element.text.strip()

        released_year = movie.select_one('.cli-title-metadata-item:nth-child(1)').text
        released_year = int(released_year)

        running_time = movie.select_one('.cli-title-metadata-item:nth-child(2)').text
        running_time = running_time.replace("h", "").replace("m", "")
        hours, minutes = running_time.split(" ")
        running_time_minutes = int(hours) * 60 + int(minutes)

        pg_level = movie.select_one('.cli-title-metadata-item:nth-child(3)').text

        doc = {
            'title': title,
            'released_year': released_year,
            'running_time_minutes': running_time_minutes,
            'pg_level': pg_level
        }

        db.movies.insert_one(doc)

        print("저장 완료:", title)

if __name__ == '__main__':
    insert_all()
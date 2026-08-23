from pymongo import MongoClient
client = MongoClient('mongodb://test:test@localhost',27017)
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbjungle

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/memo', methods=['GET'])
def listing():
    articles = list(db.articles.find({}, {'_id': False}).sort('created_at', -1))
    return jsonify({'result': 'success', 'articles': articles})

## API 역할을 하는 부분
@app.route('/memo', methods=['POST'])
def post_article():
    # 1. 클라이언트로부터 데이터를 받기
    url_receive = request.form['url_give'].strip()
    comment_receive = request.form['comment_give']

    same_article = db.articles.find_one({'url': url_receive})

    if same_article is not None:
        return jsonify({
            'result': 'fail',
            'msg': '이미 저장된 기사입니다.'
        })

    # 2. meta tag를 스크래핑하기
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    print("og_title:", og_title)
    print("og_description:", og_description)
    print("og_image:", og_image)

    if og_title is None or og_description is None or og_image is None:
        return jsonify({
            'result': 'fail',
            'msg': '메타태그를 찾지 못했습니다. 다른 URL로 테스트해보세요.'
        })

    url_title = og_title['content']
    url_description = og_description['content']
    url_image = og_image['content']

    article = {
    'url': url_receive,
    'title': url_title,
    'desc': url_description,
    'image': url_image,
    'comment': comment_receive,
    'created_at': time.time()
    }
    # 3. mongoDB에 데이터를 넣기
    db.articles.insert_one(article)

    return jsonify({'result': 'success', 'msg': '저장 완료!'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)
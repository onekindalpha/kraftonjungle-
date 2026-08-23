import requests
from bs4 import BeautifulSoup
from bson.objectid import ObjectId
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client.dbjungle


@app.route('/')
def home():
    return render_template('index.html')

#완성본을 추가
@app.route('/complete')
def complete():
    return render_template('complete.html')

# 여기에 /memo POST route 추가
@app.route('/memo', methods=['POST'])
def save_memo():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    data = requests.get(url_receive, headers=headers, timeout=5)
    data.encoding = data.apparent_encoding

    soup = BeautifulSoup(data.text, "html.parser")

    title = soup.select_one('meta[property="og:title"]')
    desc = soup.select_one('meta[property="og:description"]')
    image = soup.select_one('meta[property="og:image"]')

    title_receive = title["content"] if title and title.get("content") else "제목 없음"
    desc_receive = desc["content"] if desc and desc.get("content") else "설명 없음"
    image_receive = image["content"] if image and image.get("content") else ""

    if image_receive.startswith("//"):
        image_receive = "https:" + image_receive

    doc = {
        "url": url_receive,
        "title": title_receive,
        "desc": desc_receive,
        "image": image_receive,
        "comment": comment_receive
    }

    print("저장할 doc:", doc)

    db.articles.insert_one(doc)

    return jsonify({"msg": "저장 완료!"})
# 여기에 /memo GET route 추가
@app.route('/memo', methods=['GET'])
def read_memo():
    articles = list(db.articles.find({}).sort('_id', -1))

    for article in articles:
        article['_id'] = str(article['_id'])

    return jsonify({'articles': articles})

@app.route('/memo/delete', methods=['POST'])
def delete_memo():
    id_receive = request.form['id_give']

    db.articles.delete_one({'_id': ObjectId(id_receive)})

    return jsonify({'msg': '삭제 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)
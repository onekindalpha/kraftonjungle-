from bson import ObjectId # pymongo가 설치될 때 함께 설치됨. (install X)
from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
from flask.json.provider import JSONProvider

import json
import sys


app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.jungle_practice_safe


#####################################################################################
# 이 부분은 코드를 건드리지 말고 그냥 두세요. 코드를 이해하지 못해도 상관없는 부분입니다.
#
# ObjectId 타입으로 되어있는 _id 필드는 Flask 의 jsonify 호출시 문제가 된다.
# 이를 처리하기 위해서 기본 JsonEncoder 가 아닌 custom encoder 를 사용한다.
# Custom encoder 는 다른 부분은 모두 기본 encoder 에 동작을 위임하고 ObjectId 타입만 직접 처리한다.
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class CustomJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, **kwargs, cls=CustomJSONEncoder)

    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)


# 위에 정의되 custom encoder 를 사용하게끔 설정한다.
app.json = CustomJSONProvider(app)

# 여기까지 이해 못해도 그냥 넘어갈 코드입니다.
# #####################################################################################



#####
# 아래의 각각의 @app.route 은 RESTful API 하나에 대응됩니다.
# @app.route() 의 첫번째 인자는 API 경로,
# 생략 가능한 두번째 인자는 해당 경로에 적용 가능한 HTTP method 목록을 의미합니다.

# API #1: HTML 틀(template) 전달
#         틀 안에 데이터를 채워 넣어야 하는데 이는 아래 이어지는 /api/list 를 통해 이루어집니다.
@app.route('/')
def home():
    return render_template('index.html')


# API #2: 휴지통에 버려지지 않은 영화 목록을 반환합니다.
@app.route('/api/list', methods=['GET'])
def show_movies():
    sortMode = request.args.get('sortMode', 'likes')

    normal_filter = {
        '$or': [
            {'trashed': False},
            {'trashed': {'$exists': False}}
        ]
    }

    if sortMode == 'likes':
        movies = list(db.movies.find(normal_filter, {}).sort('likes', -1))

    elif sortMode == 'viewers':
        movies = list(db.movies.find(normal_filter, {}).sort('viewers', -1))

    elif sortMode == 'date':
        movies = list(db.movies.find(normal_filter, {}).sort([
            ('open_year', -1),
            ('open_month', -1),
            ('open_day', -1)
        ]))

    else:
        return jsonify({'result': 'failure'})

    return jsonify({'result': 'success', 'movies_list': movies})


# API #3: 영화에 좋아요 숫자를 하나 올립니다.
@app.route('/api/like', methods=['POST'])
def like_movie():
    movie_id = request.form['id_give']

    movie = db.movies.find_one({'_id': ObjectId(movie_id)})

    if movie is None:
        return jsonify({'result': 'failure'})

    new_likes = movie['likes'] + 1

    result = db.movies.update_one(
        {'_id': ObjectId(movie_id)},
        {'$set': {'likes': new_likes}}
    )

    if result.modified_count == 1:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'failure'})

@app.route('/api/trash', methods=['POST'])
def trash_movie():
    movie_id = request.form['id_give']

    result = db.movies.update_one(
        {'_id': ObjectId(movie_id)},
        {'$set': {'trashed': True}}
    )

    if result.modified_count == 1:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'failure'})


@app.route('/api/list/trash', methods=['GET'])
def show_trash_movies():
    movies = list(db.movies.find({'trashed': True}, {}))
    return jsonify({'result': 'success', 'movies_list': movies})


@app.route('/api/restore', methods=['POST'])
def restore_movie():
    movie_id = request.form['id_give']

    result = db.movies.update_one(
        {'_id': ObjectId(movie_id)},
        {'$set': {'trashed': False}}
    )

    if result.modified_count == 1:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'failure'})


@app.route('/api/delete', methods=['POST'])
def delete_movie():
    movie_id = request.form['id_give']

    result = db.movies.delete_one(
        {'_id': ObjectId(movie_id)}
    )

    if result.deleted_count == 1:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'failure'})
    
if __name__ == '__main__':
    print(sys.executable)
    app.run('0.0.0.0', port=5006, debug=True)
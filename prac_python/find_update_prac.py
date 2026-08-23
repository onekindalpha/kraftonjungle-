from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.jungle

db.movies.update_one(
    {'title': '매트릭스'},
    {'$set': {'released_year': 1998}}
)

target_movie = db.movies.find_one({'title': '매트릭스'}, {'_id': False})
print(target_movie)
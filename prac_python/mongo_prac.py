# from pymongo import MongoClient

# client = MongoClient("mongodb://localhost:27017/")
# # 기존 jungle 말고 새 연습용 DB 사용
# db = client.jungle_practice_safe


# db.users.insert_one({'name':'bobby','age':21})
# db.users.insert_one({'name':'kay','age':27})
# db.users.insert_one({'name':'john','age':30})

# # MongoDB에서 데이터 모두 보기
# all_users = list(db.users.find({}))

# # mongodb에서 특정 조건의 데이터 모두 보기
# same_ages = list(db.users.find({'age':21}))

# # 0번재 결과값을 보기
# print(all_users[0])
# # 0번째 결과값의 name을 보기
# print(all_users[0]['name'])
# # 0번째 결과값의 age를 보기
# print(all_users[0]['age'])

# # # 반복문을 돌며 모든 결과값을 보기
# # for user in all_users:
# #     print(user)

# # #특정 결과 값을 뽑아 보기
# # user = db.users.find_one({'name':'bobby'})
# # print(user)

# # 그 중 특정 키 값을 빼고 보기
# # user = db.users.find_one({'name':'bobby'}, {'_id':False})
# # print(user)


# # 생김새
# #db.people.update_many(찾을조건, { '$set': 어떻게바꿀지 })

# # # 오타가 많으니 이 줄을 복사해서 쓸 것
# # db.users.update_one({'name':'bobby'},{'$set':{'age':19}})

# # user = db.users.find_one({'name':'bobby'})
# # print(user)

# db.users.delete_one({'name':'bobby'})

# user = db.users.find_one({'name':'bobby'})
# print(user) # 삭제 처리되어 'None'으로 출력됩니다.

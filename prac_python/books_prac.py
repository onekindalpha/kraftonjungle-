from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.jungle

# Q1. 책 하나 찾기
book = db.books.find_one(
    {"title": "A Light in the Attic"},
    {"_id": False}
)

print("=== Q1. 책 하나 찾기 ===")
print(book)


# Q2. 그 책의 가격만 출력하기
print("=== Q2. 가격만 출력 ===")
print(book["price"])


# Q3. Soumission 책 찾기
soumission = db.books.find_one(
    {"title": "Soumission"},
    {"_id": False}
)

print("=== Q3. Soumission 찾기 ===")
print(soumission)


# Q4. Soumission의 stock을 Sold out으로 수정하기
db.books.update_one(
    {"title": "Soumission"},
    {"$set": {"stock": "Sold out"}}
)

updated_book = db.books.find_one(
    {"title": "Soumission"},
    {"_id": False}
)

print("=== Q4. Soumission 수정 후 ===")
print(updated_book)


# Q5. stock이 Sold out인 책만 찾기
sold_out_books = list(db.books.find(
    {"stock": "Sold out"},
    {"_id": False}
))

print("=== Q5. Sold out 책 찾기 ===")
for book in sold_out_books:
    print(book)


# Q6. Soumission 삭제하기
db.books.delete_one({"title": "Soumission"})

deleted_book = db.books.find_one(
    {"title": "Soumission"},
    {"_id": False}
)

print("=== Q6. Soumission 삭제 후 ===")
print(deleted_book)
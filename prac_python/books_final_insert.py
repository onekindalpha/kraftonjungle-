from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.jungle_practice_safe

TARGET_TITLE = "A Light in the Attic"


# Q1. 책 제목 'A Light in the Attic'의 가격 가져오기
def q1():
    target_book = db.books.find_one({"title": TARGET_TITLE})

    if target_book is None:
        print("Q1. 해당 책을 찾지 못했습니다.")
        return

    print("Q1. 가격:", target_book["price"])


# Q2. 'A Light in the Attic'과 같은 별점의 책 제목들 가져오기
def q2():
    target_book = db.books.find_one({"title": TARGET_TITLE})

    if target_book is None:
        print("Q2. 해당 책을 찾지 못했습니다.")
        return

    target_rating = target_book["rating"]

    books = list(db.books.find({"rating": target_rating}))

    print(f"Q2. '{TARGET_TITLE}'과 같은 별점({target_rating})의 책들:")

    for book in books:
        print(book["title"])


# Q3. 'A Light in the Attic'의 가격을 19.99로 만들기
def q3():
    result = db.books.update_one(
        {"title": TARGET_TITLE},
        {"$set": {"price": 19.99}}
    )

    print("Q3. 수정된 개수:", result.modified_count)

    target_book = db.books.find_one({"title": TARGET_TITLE})

    if target_book is None:
        print("Q3. 해당 책을 찾지 못했습니다.")
        return

    print("Q3. 수정 후 가격:", target_book["price"])


if __name__ == "__main__":
    q1()
    print("--------------------")

    q2()
    print("--------------------")

    q3()
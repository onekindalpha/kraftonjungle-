# app_annotated_interview.py
# 면접 복습용 각주 버전입니다.
# 제출본이 아니라, 각 route가 어떤 요청을 받고 어떤 DB 작업을 하는지 설명하기 위한 파일입니다.

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

# [각주 1] Flask 서버 객체 생성
# 브라우저 요청을 받을 서버 프로그램을 만든다.
app = Flask(__name__)

# [각주 2] MongoDB 연결
# EC2 환경에서는 test:test 계정과 authSource=admin을 포함한 인증 문자열이 필요했다.
# 실제 서비스라면 DB 계정 정보는 코드가 아니라 환경변수로 분리하는 것이 좋다.
client = MongoClient('mongodb://test:test@localhost:27017/?authSource=admin')
db = client.dbjungle


# [각주 3] 기본 화면 route
# 사용자가 / 주소로 접속하면 templates 폴더의 index_annotated_interview.html을 브라우저에 보낸다.
# render_template은 HTML 응답을 보내는 Flask 함수다.
@app.route("/")
def home():
    return render_template("index_annotated_interview.html")


# [각주 4] Create: 메모 저장 route
# 프론트의 saveMemo()가 /memo로 POST 요청을 보내면 실행된다.
# request.form으로 title_give, content_give 값을 받는다.
# MongoDB에는 likes 초기값을 0으로 넣어 새 문서 1개를 저장한다.
@app.route("/memo", methods=["POST"])
def create_memo():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    doc = {
        "title": title_receive,
        "content": content_receive,
        "likes": 0
    }

    db.memos.insert_one(doc)

    # [각주 5] jsonify
    # Python dict를 브라우저가 받을 수 있는 JSON 응답으로 바꾼다.
    # msg는 문법이 아니라 성공 메시지를 담기 위해 정한 key 이름이다.
    return jsonify({"msg": "포스팅 성공!"})


# [각주 6] Read: 메모 목록 조회 route
# 프론트의 showMemos()가 /memo로 GET 요청을 보내면 실행된다.
# find({})로 전체 메모를 조회하고, sort("likes", -1)로 좋아요 내림차순 정렬한다.
@app.route("/memo", methods=["GET"])
def read_memos():
    memos = list(db.memos.find({}).sort("likes", -1))

    # [각주 7] ObjectId 문자열 변환
    # MongoDB의 _id는 ObjectId 타입이라 JSON으로 바로 보내기 어렵다.
    # 브라우저로 보내기 전에 문자열로 바꾼다.
    for memo in memos:
        memo["_id"] = str(memo["_id"])

    return jsonify({"memos": memos})


# [각주 8] Update: 좋아요 증가 route
# 프론트의 likeMemo(id)가 /memo/like로 POST 요청을 보내면 실행된다.
# 브라우저에서 받은 id는 문자열이라 ObjectId로 변환한 뒤 MongoDB 문서를 찾는다.
# $inc는 숫자 필드를 증가시키는 MongoDB 연산자다.
@app.route("/memo/like", methods=["POST"])
def like_memo():
    id_receive = request.form["id_give"]

    db.memos.update_one(
        {"_id": ObjectId(id_receive)},
        {"$inc": {"likes": 1}}
    )

    return jsonify({"msg": "좋아요!"})


# [각주 9] Delete: 메모 삭제 route
# 프론트의 deleteMemo(id)가 /memo/delete로 POST 요청을 보내면 실행된다.
# ObjectId로 해당 문서를 찾아 delete_one으로 삭제한다.
@app.route("/memo/delete", methods=["POST"])
def delete_memo():
    id_receive = request.form["id_give"]

    db.memos.delete_one({"_id": ObjectId(id_receive)})

    return jsonify({"msg": "삭제 완료!"})


# [각주 10] Update: 메모 수정 route
# 프론트의 saveEdit(id)가 /memo/edit로 POST 요청을 보내면 실행된다.
# id, 새 제목, 새 내용을 받고 $set으로 title과 content를 변경한다.
@app.route("/memo/edit", methods=["POST"])
def edit_memo():
    id_receive = request.form["id_give"]
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    db.memos.update_one(
        {"_id": ObjectId(id_receive)},
        {
            "$set": {
                "title": title_receive,
                "content": content_receive
            }
        }
    )

    return jsonify({"msg": "수정 완료!"})


# [각주 11] 서버 실행 설정
# 0.0.0.0은 외부 접속을 받을 수 있게 모든 네트워크 인터페이스에서 요청을 받겠다는 뜻이다.
# debug=True는 개발 중에는 편하지만, 실제 배포 환경에서는 끄는 것이 좋다.
if __name__ == "__main__":
    app.run("0.0.0.0", port=5001, debug=True)

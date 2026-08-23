from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient('mongodb://test:test@localhost:27017/?authSource=admin')
db = client.dbjungle


@app.route("/")
def home():
    return render_template("index.html")


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

    return jsonify({"msg": "포스팅 성공!"})


@app.route("/memo", methods=["GET"])
def read_memos():
    memos = list(db.memos.find({}).sort("likes", -1))

    for memo in memos:
        memo["_id"] = str(memo["_id"])

    return jsonify({"memos": memos})


@app.route("/memo/like", methods=["POST"])
def like_memo():
    id_receive = request.form["id_give"]

    db.memos.update_one(
        {"_id": ObjectId(id_receive)},
        {"$inc": {"likes": 1}}
    )

    return jsonify({"msg": "좋아요!"})


@app.route("/memo/delete", methods=["POST"])
def delete_memo():
    id_receive = request.form["id_give"]

    db.memos.delete_one({"_id": ObjectId(id_receive)})

    return jsonify({"msg": "삭제 완료!"})


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


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)

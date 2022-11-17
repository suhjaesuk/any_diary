import hashlib
import datetime
import jwt
import certifi
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, Blueprint

app = Flask(__name__)


ca = certifi.where()
client = MongoClient(
    "mongodb+srv://test:qwer1234@cluster0.hju0g3t.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.anyDiary

SECRET_KEY = 'SPARTAAAAA!!!'


bp = Blueprint('content', __name__, url_prefix='/')

# db에서 가져온 content정보에서
# date를 "년 월 일 시:분:초" 형식으로 바꿔줌
#parameter : content
# 파라미터는 글에 대한 정보 전체를 넣어 줘야 함


def date_forming(content_info):
    if type(content_info.get('date', '')) is str:
        temp_arr = content_info.get('date', "").split(' ')
        if len(temp_arr) >= 5:
            temp_date = ' '.join(
                [temp_arr[3], temp_arr[1], temp_arr[2], temp_arr[4]])
            content_info['date'] = temp_date
            temp_arr = []
    return content_info


@bp.route('/readContent', methods=["GET"])
def read():
    # 게시글 정보 가져오기
    contentId = int(request.args.get('id'))
    content_info = db.contents.find_one({'contentId': contentId})
    content_info = date_forming(content_info)

    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"userId": payload['userId']})
        return render_template('readContent.html', username=user_info["username"], content=content_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return render_template('readContent.html', content=content_info)


@bp.route('/searchLike', methods=["POST"])
def searchLike_post():

    like_in_db = list(db.likes.find({}, {'_id': False}))
    like_info = {}
    # 해당 유저가 해당 글에 좋아요 클릭했는지 판별
    like_info['clicked'] = False

    count = 0
    for like in like_in_db:
        if like['contentId'] == request.form['contentId']:
            count += 1
            if like['userId'] == request.form['userId']:
                like_info['clicked'] = True
    like_info['count'] = count  # 전체 좋아요 수
    return jsonify({'click': like_info['clicked'], 'count': like_info['count']})


@bp.route('/addLike', methods=["POST"])
def addLike_post():

    contentId = request.form['contentId']
    userId = request.form['userId']
    doc = {'userId': userId, 'contentId': contentId}
    db.likes.insert_one(doc)
    return jsonify({'state': 'like'})


@bp.route('/delLike', methods=["POST"])
def delLike_post():

    contentId = request.form['contentId']
    userId = request.form['userId']
    db.likes.delete_one({'userId': userId, 'contentId': contentId})
    return jsonify({'state': 'unlike'})


@bp.route('/home', methods=["POST"])
def deleteContent_post():

    contentId = int(request.form['contentId'])
    db.contents.delete_one({'contentId': contentId})

    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"userId": payload['userId']})
        return render_template('index.html', username=user_info["username"])
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return render_template('index.html')


@bp.route('/modiContent', methods=["POST"])
def modiContent_post():
    # 게시글 정보 가져오기

    contentId = int(request.form['contentId'])
    content_info = db.contents.find_one({'contentId': contentId})
    temp_date = content_info['date']
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"userId": payload['userId']})
        return render_template('modiDiary.html', username=user_info["username"],userId=user_info["username"], content=content_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return render_template('modiDiary.html', content=content_info)


@bp.route('/modiSave', methods=["POST"])
def modiContent_save():

    contentId = int(request.form['contentId'])
    db.contents.update_one(
        {'contentId': contentId},
        {"$set":
         {'title': request.form['title'],
          'content': request.form['content'],
          'emoticon': request.form['emoticon']
          }})
    content_info = db.contents.find_one({'contentId': contentId})
    content_info = date_forming(content_info)
    return render_template('/readContent.html', content=content_info)
from flask import Flask, render_template, request, jsonify, Blueprint
from pymongo import MongoClient
from random import randint
import certifi


app = Flask(__name__)

import jwt
import datetime
import hashlib
from random import randint

SECRET_KEY = 'SPARTAAAAA!!!'

bp = Blueprint('post', __name__, url_prefix='/')
@bp.route('/writeDiary')
def write_diary():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"userId": payload['userId']})
        return render_template('postDiary.html', username=user_info["username"])
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return render_template('postDiary.html')

@bp.route('/postDiary', methods=['POST'])
def post_diary():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    date_receive = request.form['date_give']
    emoticon_receive = request.form['emoticon_give']
    username_receive = request.form['username_give']
    userId_receive = request.form['userId_give']

    countId = list(db.contents.find({},{'_id':False}))
    contentId = len(countId) + randint(0,1000)

    doc = {
        'title' : title_receive,
        'content' : content_receive,
        'date' : date_receive,
        'contentId' : contentId,
        'emoticon' : emoticon_receive,
        'username' : username_receive,
        'userId': userId_receive
    }
    db.contents.insert_one(doc)

    return jsonify({'msg' : '일기가 저장되었습니다.'})

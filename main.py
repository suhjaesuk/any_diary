from flask import Flask, render_template, jsonify, request,Blueprint

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca=certifi.where()
client = MongoClient("mongodb+srv://test:qwer1234@cluster0.hju0g3t.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.anyDiary

SECRET_KEY = 'SPARTAAAAA!!!'

import jwt
import datetime
import hashlib

bp = Blueprint('main', __name__, url_prefix='/')
def date_forming(content_info):
    if type(content_info.get('date', '')) is str:
        temp_arr = content_info.get('date', "").split(' ')
        if len(temp_arr) >= 5:
            temp_date = ' '.join([temp_arr[3], temp_arr[1], temp_arr[2], temp_arr[4]])
            content_info['date'] = temp_date
            temp_arr = []
    return content_info
@bp.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.testUser.find_one({"userId": payload['userId']})
        return render_template('index.html', username=user_info["username"])
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return render_template('index.html')


@bp.route('/list', methods=['GET'])
def list_diary():
    list_diary = list(db.testContent.find({}, {'_id': False}))
    new_list = []
    for i in list_diary:
        new_list.append(date_forming(i))
    return jsonify({'result':'success', 'list_diary': new_list})

# if __name__ == '__main__':
#     app.run('0.0.0.0', port=5000, debug=True)
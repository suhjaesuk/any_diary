import hashlib
import datetime
import jwt
import certifi
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, Blueprint

app = Flask(__name__)

ca = certifi.where()

SECRET_KEY = 'SPARTAAAAA!!!'

bp = Blueprint('login', __name__, url_prefix='/')

# @bp.route('/')
# def home():
#
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         user_info = db.users.find_one({"userId": payload['userId']})
#         return render_template('index.html', username=user_info["username"])
#     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
#         return render_template('index.html')


@bp.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@bp.route('/register')
def register():
    return render_template('register.html')


#####  로그인을 위한 API  ######

# [회원가입 API]
# id, pw, username을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.

@bp.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    username_receive = request.form['username_give']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    db.users.insert_one(
        {'userId': id_receive, 'password': pw_hash, 'username': username_receive})

    return jsonify({'result': 'success'})


# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.

@bp.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.users.find_one({'userId': id_receive, 'password': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'userId': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        # .decode('utf-8')
        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# [유저 정보 확인 API]
# 로그인된 유저만 call 할 수 있는 API입니다.
# 유효한 토큰을 줘야 올바른 결과를 얻어갈 수 있습니다.


@bp.route('/usertoken', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        # payload 안에 id가 들어있습니다. id로 유저정보를 찾습니다.
        userinfo = db.users.find_one({'userId': payload['userId']}, {'_id': 0})
        return jsonify({'result': 'success', 'username': userinfo['username'], 'userId': userinfo['userId']})

    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


# userid find one 하는게 더 나을것 같다.
@bp.route('/api/checkid', methods=['POST'])
def c_id():
    chk_id = 0
    id_receive = request.form['id_give']
    users = list(db.users.find({}, {'_id': False}))

    for user in users:
        user_id = user['userId']
        if user_id == id_receive:
            chk_id = 1

    return jsonify({'result': 'success', 'status': chk_id})

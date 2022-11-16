from flask import Flask, render_template, jsonify, request, redirect

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

def check_login():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.testUser.find_one({"userId": payload['userId']})
        return user_info["username"]
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return null

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.testUser.find_one({"userId": payload['userId']})
        return render_template('index.html', username=user_info["username"])
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return render_template('index.html')

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return redirect('/')

@app.route('/list', methods=['GET'])
def show_diary():
    show_diary = list(db.testContent.find({}, {'_id': False}))
    return jsonify({'result':'success', 'show_diary': show_diary})


@app.route('/writeDiary')
def write_diary():
    return render_template('postDiary.html')

@app.route('/postDiary', methods=['POST'])
def post_diary():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    # username_receive = request.form['username_give']
    date_receive = request.form['date_give']
    emoticon_receive = request.form['emoticon_give']

    countId = list(db.testContent.find({},{'_id':False}))
    num = len(countId) + 1

    doc = {
        'title' : title_receive,
        'content' : content_receive,
        # 'username' : username_receive,
        'date' : date_receive,
        'num' : num,
        'emoticon' : emoticon_receive


    }
    db.testContent.insert_one(doc)
    return jsonify({'msg' : '일기가 저장되었습니다.'})
#####  로그인을 위한 API  ######

# [회원가입 API]
# id, pw, username을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.testUser.insert_one({'userId': id_receive, 'password': pw_hash, 'username': nickname_receive})

    return jsonify({'result': 'success'})


# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.testUser.find_one({'userId': id_receive, 'password': pw_hash})

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

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# [유저 정보 확인 API]
# 로그인된 유저만 call 할 수 있는 API입니다.
# 유효한 토큰을 줘야 올바른 결과를 얻어갈 수 있습니다.

@app.route('/api/username', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        # payload 안에 id가 들어있습니다. id로 유저정보를 찾습니다.
        userinfo = db.testUser.find_one({'userId': payload['userId']}, {'_id': 0})
        return jsonify({'result': 'success',
                        'username': userinfo['username'],
                        'userId':userinfo['userId']})

    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

#db에서 가져온 content정보에서
#date를 "년 월 일 시:분:초" 형식으로 바꿔줌
#parameter : content
#파라미터는 글에 대한 정보 전체를 넣어 줘야 함
def date_forming(content_info):
    if type(content_info.get('date', '')) is str:
        temp_arr = content_info.get('date', "").split(' ')
        if len(temp_arr) >= 5:
            temp_date = ' '.join([temp_arr[3], temp_arr[1], temp_arr[2], temp_arr[4]])
            content_info['date'] = temp_date
            temp_arr = []
    return content_info

@app.route('/readContent', methods=["GET"])
def read():

    #게시글 정보 가져오기
    contentId = int(request.args.get('contentId'))
    #contentId = request['contentId']
    #contentId = 1234
    content_info = db.testContent.find_one({'contentId': contentId})
    content_info = date_forming(content_info)
    #게시글 좋아요 정보 가져오기
    like_in_db = list(db.testLike.find({}, {'_id': False}))
    like_info = {}
    #해당 유저가 해당 글에 좋아요 클릭했는지 판별
    # like_info['clicked'] = False
    # for like in like_in_db:
    #     if like['contentId'] == request.args.get('contentId') and like['userId'] == request.form['userId']:
    #     #if like['contentId'] == '1234' and like['userId'] == 'test':
    #         like_info['clicked'] = True
    #
    # like_info['count'] = len(like_in_db) #전체 좋아요 수
    return render_template('readContent.html', content = content_info)



@app.route('/searchLike', methods=["POST"])
def searchLike_post():
    like_in_db = list(db.testLike.find({}, {'_id': False}))
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
    return jsonify({'click': like_info['clicked'], 'count':like_info['count']})

@app.route('/addLike', methods=["POST"])
def addLike_post():
    print(request.form['contentId'])
    print(request.form['userId'])
    contentId = request.form['contentId']
    userId = request.form['userId']
    doc = {'userId': userId, 'contentId' : contentId}
    db.testLike.insert_one(doc)
    return jsonify({'state': 'like'})

@app.route('/delLike', methods=["POST"])
def delLike_post():
    print(request.form['contentId'], request.form['userId'])
    contentId = request.form['contentId']
    userId = request.form['userId']
    db.testLike.delete_one({'userId': userId, 'contentId':contentId})
    return jsonify({'state':'unlike'})

@app.route('/deleteContent', methods=["POST"])
def deleteContent_post():

    contentId = int(request.form['contentId'])
    db.testContent.delete_one({'contentId':contentId})
    return render_template('/index.html')

@app.route('/modiContent', methods=["POST"])
def modiContent_post():
    # 게시글 정보 가져오기
    print('modiContent')
    contentId = int(request.form['contentId'])
    print('contentId', contentId)
    content_info = db.testContent.find_one({'contentId': contentId})
    print(content_info)
    temp_date = content_info['date']
    print(temp_date)
    #date = temp_date.strftime("%Y-%m-%d")  # 날짜 파싱
    #content_info['date'] = date

    return render_template('modiDiary.html', content = content_info)

@app.route('/modiSave', methods=["POST"])
def modiContent_save():
    print('modi save')
    print(request.form)
    contentId = int(request.form['contentId'])
    #db.testContent.update(({'contentId': contentId},{'$set': doc}))
    db.testContent.update_one(
        {'contentId': contentId},
        {"$set":
             {'title': request.form['title'],
           'content' : request.form['content'],
           'emoticon' : request.form['emoticon']
              }})

    content_info = db.testContent.find_one({'contentId': contentId})
    content_info = date_forming(content_info)
    return render_template('/readContent.html', content=content_info)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
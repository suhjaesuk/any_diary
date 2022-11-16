from flask import Flask, render_template, jsonify, request, Blueprint

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca=certifi.where()
client = MongoClient("mongodb+srv://test:qwer1234@cluster0.hju0g3t.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.anyDiary

SECRET_KEY = 'SPARTAAAAA!!!'



bp = Blueprint('content', __name__, url_prefix='/')

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

@bp.route('/readContent', methods=["GET"])
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



@bp.route('/searchLike', methods=["POST"])
def searchLike_post():
    like_in_db = list(db.testLike.find({}, {'_id': False}))
    like_info = {}
    # 해당 유저가 해당 글에 좋아요 클릭했는지 판별
    like_info['clicked'] = False
    print('들어옴')
    print(request.form)
    count = 0
    for like in like_in_db:
        if like['contentId'] == request.form['contentId']:
            count += 1
            if like['userId'] == request.form['userId']:
                like_info['clicked'] = True
    like_info['count'] = count  # 전체 좋아요 수
    return jsonify({'click': like_info['clicked'], 'count':like_info['count']})

@bp.route('/addLike', methods=["POST"])
def addLike_post():
    print(request.form['contentId'])
    print(request.form['userId'])
    contentId = request.form['contentId']
    userId = request.form['userId']
    doc = {'userId': userId, 'contentId' : contentId}
    db.testLike.insert_one(doc)
    return jsonify({'state': 'like'})

@bp.route('/delLike', methods=["POST"])
def delLike_post():
    print(request.form['contentId'], request.form['userId'])
    contentId = request.form['contentId']
    userId = request.form['userId']
    db.testLike.delete_one({'userId': userId, 'contentId':contentId})
    return jsonify({'state':'unlike'})

@bp.route('/deleteContent', methods=["POST"])
def deleteContent_post():
    print(request.form['contentId'])
    contentId = request.form['contentId']
    db.testLike.delete_one({'contentId':contentId})
    return render_template('/')

@bp.route('/modiContent', methods=["POST"])
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

@bp.route('/modiSave', methods=["POST"])
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
    return render_template('/')

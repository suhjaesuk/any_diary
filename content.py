from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi

ca = certifi.where()
url = 'mongodb+srv://test:qwer1234@cluster0.hju0g3t.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(url, tlsCAFile  = ca)
db = client.anyDiary

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

#Content내용 가져오기
@app.route('/readContent', methods=["GET"])
def read():
    #print(request)
    #print(request['contentId'])
    #contentId = request['contentId']

    #게시글 정보 가져오기
    content_info = db.testContent.find_one({'contentId':1234})
    temp_date = content_info['date']
    date = temp_date.strftime("%Y년 %m월 %d일 %X") #날짜 파싱
    content_info['date'] = date

    #게시글 좋아요 정보 가져오기
    like_in_db = list(db.testLike.find({}, {'_id': False}))
    print(like_in_db)
    like_info = {}
    #해당 유저가 해당 글에 좋아요 클릭했는지 판별
    like_info['clicked'] = False
    for like in like_in_db:
        #if like['contentId'] == request['contentId'] and like['userId'] == request['userId']:
        if like['contentId'] == '1234' and like['userId'] == 'test':
            like_info['clicked'] = True

    like_info['count'] = len(like_in_db) #전체 좋아요 수
    print(like_info)
    return render_template('readContent.html', content = content_info, like = like_info)


@app.route('/searchLike', methods=["GET"])
def searchLike_post():
    like_in_db = list(db.testLike.find({}, {'_id': False}))
    like_info = {}
    # 해당 유저가 해당 글에 좋아요 클릭했는지 판별
    like_info['clicked'] = False
    for like in like_in_db:
        # if like['contentId'] == request['contentId'] and like['userId'] == request['userId']:
        if like['contentId'] == '1234' and like['userId'] == 'test':
            like_info['clicked'] = True
    like_info['count'] = len(like_in_db)  # 전체 좋아요 수
    return jsonify({'click': like_info['clicked'], 'count':like_info['count']})

@app.route('/addLike', methods=["POST"])
def addLike_post():
    print(request.form['contentId'])
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
    print(request.form['contentId'])
    contentId = request.form['contentId']
    db.testLike.delete_one({'contentId':contentId})
    return jsonify({'state':'게시글 삭제'})

@app.route('/modiContent', methods=["POST"])
def modiContent_post():
    # 게시글 정보 가져오기
    print('modiContent')
    contentId = int(request.form['contentId'])
    print('contentId', contentId)
    content_info = db.testContent.find_one({'contentId': contentId})
    print(content_info)
    temp_date = content_info['date']
    date = temp_date.strftime("%Y-%m-%d")  # 날짜 파싱
    content_info['date'] = date

    return render_template('modiDiary.html', content = content_info)

@app.route('/modiSave', methods=["POST"])
def modiContent_save():
    print('modi save')
    print(request.form)
    contentId = int(request.form['contentId'])
    doc = {'title': request.form['title'],
           'content' : request.form['content'],
           'date' : request.form['date'],
           'emoticon' : request.form['emoticon']}
    #db.testContent.update(({'contentId': contentId},{'$set': doc}))
    db.testContent.update_one(
        {'contentId': contentId},
        {"$set":
             {'title': request.form['title'],
           'content' : request.form['content'],
           'date' : request.form['date'],
           'emoticon' : request.form['emoticon']
              }})
    return jsonify({'state':'게시글 수정 저장'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
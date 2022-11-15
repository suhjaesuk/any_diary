from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:qwer1234@cluster0.hju0g3t.mongodb.net/?retryWrites=true&w=majority')
db = client.anyDiary

app = Flask(__name__)


""" @app.route('/')
def home():
    return render_template('index.html') """
    
@app.route('/showDiary')
def show_diary():
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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

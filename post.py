from flask import Flask, render_template, request, jsonify, Blueprint
from pymongo import MongoClient
import certifi
ca=certifi.where()
client = MongoClient("mongodb+srv://test:qwer1234@cluster0.hju0g3t.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db = client.anyDiary

app = Flask(__name__)


bp = Blueprint('post', __name__, url_prefix='/')
@bp.route('/writeDiary')
def write_diary():
    return render_template('postDiary.html')

@bp.route('/postDiary', methods=['POST'])
def post_diary():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    date_receive = request.form['date_give']
    emoticon_receive = request.form['emoticon_give']
    username_receive = request.form['username_give']


    countId = list(db.testContent.find({},{'_id':False}))
    num = len(countId) + 1

    doc = {
        'title' : title_receive,
        'content' : content_receive,
        'date' : date_receive,
        'num' : num,
        'emoticon' : emoticon_receive,
        'username' : username_receive,
        'emoticon' : emoticon_receive
    }
    db.testContent.insert_one(doc)

    return jsonify({'msg' : '일기가 저장되었습니다.'})

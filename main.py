from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient(
    'mongodb+srv://test:qwer1234@cluster0.hju0g3t.mongodb.net/?retryWrites=true&w=majority')
db = client.anyDiary

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/list', methods=['GET'])
def list_diary():
    list_diary = list(db.testContent.find({}, {'_id': False}))
    new_list = []
    for i in list_diary:
        new_list.append(date_forming(i))
    return jsonify({'result':'success', 'list_diary': new_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
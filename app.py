from flask import Flask,render_template

app = Flask(__name__)

import main, login, content, post

app.register_blueprint(main.bp)
app.register_blueprint(login.bp)
app.register_blueprint(content.bp)
app.register_blueprint(post.bp)


@app.errorhandler(Exception)
def page_not_found(error):
     return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
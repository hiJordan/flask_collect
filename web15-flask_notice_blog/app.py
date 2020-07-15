from flask import (
    Flask,
    request,
    redirect,
    url_for,
    Blueprint,
    flash,
)
from routes.todo import main as todo_routes
from routes.notice import bp_notice as notice_routes
from routes.blog import bp_blog as blog_routes


app = Flask(__name__)
app.secret_key = 'secret key test'

app.register_blueprint(todo_routes, url_prefix='/todo')
app.register_blueprint(notice_routes, url_prefix='/notice')
app.register_blueprint(blog_routes, url_prefix='/blog')


if __name__ == '__main__':
    config = dict(
        debug=True,
        port=3000,
    )
    app.run(**config)

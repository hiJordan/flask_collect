from flask import (
    Flask,
    request,
    redirect,
    url_for,
    Blueprint,
    flash,
)
from routes.todo import main as todo_routes


app = Flask(__name__)
app.secret_key = 'secret key test'

app.register_blueprint(todo_routes, url_prefix='/todo')

if __name__ == '__main__':
    config = dict(
        debug=True,
        port=3000,
    )
    app.run(**config)

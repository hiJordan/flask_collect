from flask import (
    Flask,
)
from flask_socketio import SocketIO

socketio = SocketIO()


def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    app.secret_key = 'flask secret key test info'

    from .main import bp_main
    app.register_blueprint(bp_main)

    socketio.init_app(app)
    return app



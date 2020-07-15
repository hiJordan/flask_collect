from utils import (
    log,
    redirect,
    templates,
    http_response,
)
from models.weibo import Weibo, Comment
from models.user import User
from .session import session


def current_user(request):
    session_id = request.cookies.get('user', '')
    user_id = int(session.get(session_id, '-1'))
    u = User.find_by(id=user_id)
    return u


def index(request):
    body = templates('weibo_index.html')
    return http_response(body)


route_dict = {
    '/weibo/index': index,
}


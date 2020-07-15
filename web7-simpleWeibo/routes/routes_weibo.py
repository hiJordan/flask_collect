from utils import log
from utils import redirect
from utils import templates
from utils import http_response

from models.weibo import Weibo, Comment
from models.user import User
from .session import session


def current_user(request):
    session_id = request.cookies.get('user', '')
    user_id = int(session.get(session_id, '-1'))
    u = User.find_by(id=user_id)
    return u


def login_required(func):
    def wrap_func(request):
        user = current_user(request)
        if user is None:
            return redirect('/login')

        return func(request)

    return wrap_func


def index(request):
    user_id = int(request.query.get('user_id', -1))
    user = User.find_by(id=user_id)
    weibos = Weibo.find_all(user_id=user_id)
    body = templates('weibo_index.html', weibos=weibos, user=user)
    return http_response(body)


def add(request):
    user = current_user(request)
    form = request.form()
    weibo = Weibo(form)
    weibo.user_id = user.id
    weibo.save()
    return redirect('/weibo/index?user_id={}'.format(user.id))


def new(request):
    user = current_user(request)
    body = templates('weibo_new.html')
    return http_response(body)


def edit(request):
    weibo = Weibo.find_by(id=int(request.query.get('id', None)))
    body = templates('weibo_edit.html', weibo=weibo)
    return http_response(body)


def weibo_delete(request):
    user = current_user(request)
    weibo = Weibo.find_by(id=int(request.query.get('id', None)))
    weibo.remove()
    return redirect('/weibo/index?user_id={}'.format(user.id))


def update(request):
    user = current_user(request)
    form = request.form()
    weibo = Weibo.find_by(id=int(form.get('id', None)))
    if user.id != weibo.user_id:
        return redirect('/login')
    weibo.content = form.get('content')
    weibo.save()
    return redirect('/weibo/index?user_id={}'.format(user.id))


def comment_add(request):
    user = current_user(request)
    form = request.form()
    comment = Comment(form)
    comment.user_id = user.id
    comment.save()
    return redirect('/weibo/index?user_id={}'.format(user.id))


route_dict = {
    '/weibo/index': login_required(index),
    '/weibo/add': login_required(add),
    '/weibo/delete': login_required(weibo_delete),
    '/weibo/edit': login_required(edit),
    '/weibo/update': login_required(update),
    '/weibo/new': login_required(new),
    '/comment/add': login_required(comment_add),
}


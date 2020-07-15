import json
from routes.session import session
from utils import (
    log,
    redirect,
    http_response,
    json_response,
)

from models.weibo import Weibo, Comment


def remove_weibo(request):
    weibo_id = int(request.query.get('id'))
    weibo = Weibo.remove(weibo_id)
    return json_response(weibo.json())


def update_weibo(request):
    form = request.json()
    weibo_id = int(form.get('id'))
    weibo = Weibo.update(weibo_id, form)
    return json_response(weibo.json())


def all_weibo(request):
    weibo_list = Weibo.all()
    weibos = [weibo.json() for weibo in weibo_list]
    return json_response(weibos)


def add_weibo(request):
    form = request.json()
    weibo = Weibo.new(form)
    return json_response(weibo.json())


def add_comment(request):
    form = request.json()
    comment = Comment.new(form)
    return json_response(comment.json())


def remove_comment(request):
    comment_id = int(request.query.get('id'))
    comment = Comment.remove(comment_id)
    return json_response(comment.json())


route_dict = {
    '/api/weibo/delete': remove_weibo,
    '/api/weibo/update': update_weibo,
    '/api/weibo/all': all_weibo,
    '/api/weibo/add': add_weibo,
    '/api/weibo/comment/add': add_comment,
    '/api/weibo/comment/remove': remove_comment,
}
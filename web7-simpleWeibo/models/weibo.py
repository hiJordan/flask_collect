from models import Model
from utils import log
from models.user import User


class Weibo(Model):
    def __init__(self, form, user_id=-1):
        self.id = form.get('id', None)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', user_id)

    def comments(self):
        a = Comment.find_all(weibo_id=self.id)
        log('comments: ', a)
        return a


class Comment(Model):
    def __init__(self, form, user_id=-1):
        self.id = form.get('id', None)
        self.content = form.get('content', '')
        self.weibo_id = int(form.get('weibo_id', -1))
        self.user_id = form.get('user_id', user_id)

    def user(self):
        return User.find_by(id=self.user_id).username
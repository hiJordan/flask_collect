from models import Model
import time
from utils import log
from models.user import User


class Weibo(Model):
    def __init__(self, form):
        self.id = None
        self.content = form.get('content', '')

    def json(self):
        d = self.__dict__.copy()
        comments = [c.json() for c in self.comments()]
        d['comments'] = comments
        return d

    def comments(self):
        return Comment.find_all(weibo_id=self.id)

    @classmethod
    def update(cls, todo_id, form):
        t = cls.find(todo_id)
        valid_names = [
            'content'
        ]
        for key in form:
            if key in valid_names:
                setattr(t, key, form[key])
        t.save()
        return t


class Comment(Model):
    def __init__(self, form):
        self.id = None
        self.content = form.get('content', '')
        self.weibo_id = int(form.get('weibo_id', -1))

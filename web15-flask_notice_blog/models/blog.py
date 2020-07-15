import time
from models import Model


class Blog(Model):
    def __init__(self, form):
        self.id = None
        self.title = form.get("title", "")
        self.author = form.get("author", "")
        self.content = form.get('content', "")
        self.ct = int(time.time())

    @classmethod
    def new(cls, form):
        m = cls(form)
        m.save()
        return m


class BlogComment(Model):
    def __init__(self, form):
        self.id = None
        self.content = form.get('content', "")
        self.author = form.get('author', "")
        self.ct = int(time.time())
        self.blog_id = int(form.get("blog_id", 0))

    @classmethod
    def new(cls, form):
        m = cls(form)
        m.save()
        return m



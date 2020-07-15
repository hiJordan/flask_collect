from models import Model
import time


class Notice(Model):
    def __init__(self, form):
        self.id = None
        self.content = form.get("content", "")
        self.author = form.get("author", "")
        self.ct = int(time.time())

    @classmethod
    def new(cls, form):
        m = cls(form)
        m.save()
        return m

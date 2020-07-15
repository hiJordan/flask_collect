from models import Model
import time


class Todo(Model):
    def __init__(self, form):
        self.id = None
        self.title = form.get('title', '')
        self.completed = False
        self.ct = int(time.time())
        self.ut = self.ct

    @classmethod
    def update(cls, todo_id, form):
        t = cls.find(todo_id)
        valid_names = [
            'title',
            'completed'
        ]
        for key in form:
            if key in valid_names:
                setattr(t, key, form[key])
        t.ut = int(time.time())
        t.save()
        return t

    @classmethod
    def complete(cls, id, completed=True):
        t = cls.find(id)
        t.completed = completed
        t.save()
        return t




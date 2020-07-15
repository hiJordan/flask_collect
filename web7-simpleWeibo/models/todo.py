from models import Model
import time


class Todo(Model):
    def __init__(self, form, user_id=-1):
        self.id = form.get('id', None)
        self.task = form.get('task', '')
        self.user_id = int(form.get('user_id', user_id))
        self.create_time = form.get('create_time', None)
        self.update_time = form.get('update_time', None)
        if self.create_time is None:
            self.create_time = self.ct()
            self.update_time = self.create_time

    def ct(self):
        datetime_format = '%Y-%m-%d %H:%M:%S'
        value = time.localtime(time.time())
        datetime = time.strftime(datetime_format, value)
        return datetime

    @classmethod
    def new(cls, form, user_id=-1):
        m = cls(form, user_id)
        m.save()
        return m


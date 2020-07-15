from models import Model


class Todo(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.title = form.get('title', '')
        self.user_id = int(form.get('user_id', -1))
        self.create_time = form.get('create_time', 0)
        self.update_time = form.get('update_time', 0)

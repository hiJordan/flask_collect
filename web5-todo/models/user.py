from models import Model
from utils import log


class User(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        if self.id is not None:
            self.id = int(self.id)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.note = form.get('note', '')
        self.role = form.get('role', 10)

    def validate_login(self):
        """
        raw_models = self.all()
        trans_models = [m.__dict__ for m in raw_models]
        for m in trans_models:
            if self.username == m.get('username') and self.password == m.get('password'):
                return True
        return False
        """
        user = self.find_by(username=self.username)
        return user is not None and user.password == self.password

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2 and len(self.note) > 1


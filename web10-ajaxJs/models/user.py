from models import Model
import hashlib


class User(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        if self.id is not None:
            self.id = int(self.id)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.role = form.get('role', 10)

    def is_admin(self):
        return self.role == 1

    def salted_password(self, pwd, salt='#$!#%KLjf-$=ofw][|'):
        def sha256(ascii_str):
            return hashlib.sha256(pwd.encode('ascii')).hexdigest()
        hash1 = sha256(pwd)
        hash2 = sha256(hash1 + salt)
        return hash2

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
        if user is not None:
            return user.password == self.salted_password(self.password)
        else:
            return False

    def validate_register(self):
        pwd = self.password
        self.password = self.salted_password(pwd)
        if User.find_by(username=self.username) is None:
            self.save()
            return self
        else:
            return None



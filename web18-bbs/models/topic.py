from models import Model
import time


class Topic(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', None)
        self.ct = int(time.time())
        self.ut = self.ct
        self.views = form.get('views', 0)

    @classmethod
    def get(cls, id):
        m = cls.find(id)
        m.views += 1
        m.save()
        return m

    def replies(self):
        from models.reply import Reply
        all_reply = Reply.find_all(topic_id=self.id)
        return all_reply
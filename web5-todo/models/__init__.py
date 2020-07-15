from utils import log
import json


def save(data, path):
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        log('Save: ', path, data, s, )
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('Load: ', s)
        return json.loads(s)


class Model(object):

    @classmethod
    def db_path(cls):
        cls_name = cls.__name__
        path = 'db/{}.txt'.format(cls_name)
        return path

    @classmethod
    def new(cls, form):
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        path = cls.db_path()
        raw_models = load(path)
        models = [cls.new(m) for m in raw_models]
        return models

    @classmethod
    def find_by(cls, **kwargs):
        log("find_by kwargs: ", kwargs)
        k, v = '', ''

        for key, value in kwargs.items():
            k, v = key, value

        for model in cls.all():
            if model.__dict__.get(k) == v:
                return model
        return None

    @classmethod
    def find_all(cls, **kwargs):
        models = []
        k, v = '', ''
        log('find_all kwargs: ', kwargs)
        for key, value in kwargs.items():
            k, v = key, value

        for model in cls.all():
            if model.__dict__.get(k) == v:
                models.append(model)
        return models

    def save(self):
        models = self.all()
        first_id = 0

        if self.__dict__.get('id') is None:
            if len(models) > 0:
                self.id = models[-1].id + 1
            else:
                self.id = first_id
            models.append(self)
        else:
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            if index > -1:
                models[index] = self

        log('Model: ', models)
        path = self.db_path()
        trans_models = [m.__dict__ for m in models]
        save(trans_models, path)

    def remove(self):
        models = self.all()
        index = -1

        for i, m in enumerate(models):
            if m.id == self.id:
                index = i
                break
        if index > -1:
            del models[index]

        log('remove after models :', models)
        path = self.db_path()
        trans_models = [m.__dict__ for m in models]
        save(trans_models, path)

    def __repr__(self):
        cls_name = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '<br>'.join(properties)
        return '< {}<br>{} ><br>'.format(cls_name, s)


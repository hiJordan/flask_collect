from utils import log
import json
import time


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


"""
def binary_search(raw_list, data):
        first = 0
        last = len(raw_list)-1

        log('bs   :', first, last)

        if last >= 1:
            mid = int(1 + (last - 1) / 2)
            log('raw_list:  ', raw_list[mid].__dict__.get('id'))
            if raw_list[mid].__dict__.get('id') == data:
                return raw_list[mid]
            elif raw_list[mid].__dict__.get('id') > data:
                return binary_search(raw_list[first:mid-1], data)
            else:
                return binary_search(raw_list[mid+1:last], data)
        else:
            return None
"""


class Model(object):

    @classmethod
    def db_path(cls):
        cls_name = cls.__name__
        path = 'db/{}.txt'.format(cls_name)
        return path

    @classmethod
    def new(cls, form):
        m = cls(form)
        m.save()
        return m

    @classmethod
    def _new_from_dict(cls, d):
        m = cls({})
        for k, v in d.items():
            setattr(m, k, v)
        return m

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    @classmethod
    def all(cls):
        path = cls.db_path()
        raw_models = load(path)
        # models = [cls(m) for m in raw_models.values()]
        models = [cls._new_from_dict(m) for m in raw_models]
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

        # return binary_search(raw_list=cls.all(), data=v)

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

    # 当前Model的字典表示
    def json(self):
        d = self.__dict__.copy()
        return d

    def save(self):
        models = self.all()

        if self.id is None:
            if len(models) == 0:
                self.id = 1
            else:
                self.id = models[-1].id + 1
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
        # trans_models = {int(m.id): m.__dict__ for m in models}
        trans_models = [m.__dict__ for m in models]
        log('trans_models: ', trans_models)
        save(trans_models, path)

    @classmethod
    def remove(cls, todo_id):
        models = cls.all()
        index = -1

        for i, m in enumerate(models):
            if m.id == todo_id:
                index = i
                break
        if index > -1:
            model = models.pop(index)
            log('remove after models :', models)
            path = cls.db_path()
            trans_models = [m.__dict__ for m in models]
            save(trans_models, path)
            return model

    def __repr__(self):
        cls_name = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '<br>'.join(properties)
        return '< {}<br>{} ><br>'.format(cls_name, s)


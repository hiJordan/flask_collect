import json


class JSON_RPC(object):
    def __init__(self):
        self.data = None

    def from_data(self, data):
        self.data = json.loads(data.decode('utf-8'))

    def call_method(self):
        method_name = self.data.get('method_name', None)
        method_args = self.data.get('method_args', None)
        method_kwargs = self.data.get('method_kwargs', None)

        getattr(self, method_name)(*method_args, **method_kwargs)

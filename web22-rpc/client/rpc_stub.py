import json


class Rpc_Stub(object):
    def __getattr__(self, item):
        def _(*args, **kwargs):
            data = {'method_name': item, 'method_args': args, 'method_kwargs': kwargs}
            self.send(json.dumps(data).encode('utf-8'))
        setattr(self, item, _)
        return _


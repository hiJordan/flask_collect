class RPC_STUB(object):
    def __init__(self):
        ...

    def test(self, a):
        print('test: ', a)

    def foo(self, a, b, c):
        print('foo: ', a, b, c)

    def bar(self, a, b, c=10):
        print('bar: ', a, b, c)

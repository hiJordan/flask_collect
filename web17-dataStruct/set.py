from collections import Iterable


class Set:
    def __init__(self, *args):
        self.data_size = 10007
        self.data = [0] * self.data_size
        self.args_len = len(args)
        self.user_args = args
        # if isinstance(args, Iterable):
        #     self.user_args = args
        # elif args_len > 1:
        #     raise Exception('TypeError: set expected at most 1 arguments, got {}'.format(args_len))
        # else:
        #     pass

    def __repr__(self):
        return self.data_add(self.user_args)

    def __eq__(self, other):
        if self.user_args == other.user_args:
            return True
        return False

    def add(self, value):
        if self.has(value):
            return
        index = self._index(value)
        values = self.data[index]
        if isinstance(values, int):
            self.data[index] = [value]
        else:
            self.data[index].append(value)
        return value

    def has(self, value):
        index = self._index(value)
        values = self.data[index]
        if isinstance(values, list):
            for v in values:
                if v == value:
                    return True
        return False

    def _index(self, value):
        return self._hash(value) % self.data_size

    def _hash(self, value):
        i = 1
        h = 1
        for v in str(value):
            h += ord(v) * i
            i *= 10
        return h

    def data_add(self, values):
        user_data = set()
        for value in values:
            v = self.add(value)
            if v is not None:
                user_data.add(v)
        self.user_args = user_data
        print(self.user_args)
        return str(user_data)

    def remove(self, value):
        print(value, self.user_args)
        # if not self.has(value):
        #     print('keyError: ', value)
        #     return
        index = self._index(value)
        values = self.data[index]
        print(self.user_args, index, type(self.data[index]))
        if isinstance(values, list):
            print(type(values), values)
            values.remove(value)
            print(values)
            self.data[index] = values
            # self.user_args =


def test():
    a = Set(1, 2, 3, 3)
    print(a)
    a.remove(1)
    # assert(a == b)
    print(a)


if __name__ == '__main__':
    test()

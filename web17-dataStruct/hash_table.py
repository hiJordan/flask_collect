class HashTable:
    def __init__(self):
        self.table_size = 10007
        self.table = [0] * self.table_size

    def __contains__(self, item):
        return self.has_key(item)

    def add(self, key, value):
        index = self._index(key)
        self._insert_at_index(index, key, value)

    def get(self, key=None):
        index = self._index(key)
        values = self.table[index]
        if isinstance(values, list):
            for v in values:
                if v[0] == key:
                    return v[1]
        return key

    def _insert_at_index(self, index, key, value):
        v = self.table[index]
        data = [key, value]
        if isinstance(v, int):
            self.table[index] = [data]
        else:
            self.table[index].append(data)

    def _index(self, key):
        return self._hash(key) % self.table_size

    def _hash(self, key):
        i = 1
        h = 1
        for k in key:
            h += ord(k) * i
            i *= 10
        return h

    def has_key(self, key):
        index = self._index(key)
        values = self.table[index]
        if isinstance(values, list):
            for v in values:
                if v[0] == key:
                    return True
        return False


def test():
    import uuid
    ht = HashTable()
    keys = [
        'python',
        'test',
        'java',
        'javascript',
        'C#',
    ]
    for key in keys:
        value = uuid.uuid4()
        ht.add(key, value)
        print('add data: ', key, value)
    for key in keys:
        value = ht.get(key)
        print('get add: ', key, value)

    print('magic method: ', 'python' in ht)


if __name__ == '__main__':
    test()

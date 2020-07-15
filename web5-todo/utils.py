import time


def log(*args, **kwargs):
    datetime_format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(time.time())
    datetime = time.strftime(datetime_format, value)
    print(datetime, *args, **kwargs)


from jinja2 import Environment, FileSystemLoader
import time
import os.path
import json


templates_dir = '{}/templates/'.format(os.path.dirname(__file__))
loader = FileSystemLoader(templates_dir)
env = Environment(loader=loader)


def templates(path, **kwargs):
    template = env.get_template(path)
    return template.render(**kwargs)


def log(*args, **kwargs):
    datetime_format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(time.time())
    datetime = time.strftime(datetime_format, value)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(datetime, *args, file=f, **kwargs)


def response_with_headers(header, code=200):
    headers = 'HTTP/1.1 {} OK\r\n'.format(code)
    headers += ''.join(['{}: {}\r\n'.format(k, v) for k, v in header.items()])
    return headers


def redirect(url, headers=None):
    header = {
        'Content-Type': 'text/html',
    }
    if headers is not None:
        header.update(headers)
    header['Location'] = url
    response = response_with_headers(header, code=302) + '\r\n'
    return response.encode('utf-8')


def http_response(body, headers=None):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    if headers is not None:
        header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])
    response = header + '\r\n' + body
    log('http response:', response)
    return response.encode('utf-8')


def error(request, code=404):
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>404 NOT FOUND PAGE</h1>'
    }

    return e.get(code, b'')


def json_response(data):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n'
    body = json.dumps(data, ensure_ascii=False, indent=2)
    r = header + '\r\n' + body
    return r.encode('utf-8')

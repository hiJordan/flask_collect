import socket
import urllib.parse
from utils import log
from routes.routes_static import route_static
from routes.routes_user import route_dict
from routes.routes_todo import route_dict as todo_route
from routes.routes_weibo import route_dict as weibo_route


# 保存请求信息，form使body转换为字典
class Request(object):
    def __init__(self):
        self.path = ''
        self.query = {}
        self.method = 'GET'
        self.header = {}
        self.cookies = {}
        self.body = ''

    def form(self):
        body = self.body.split('&')
        log("body: ", body, self.method)
        args = []
        for b in body:
            args.append(urllib.parse.unquote(b))
        f = {}

        for arg in args:
            k, v = arg.split('=')
            f[k] = v

        return f

    def add_headers(self, raw_request=None):
        if raw_request is not None:
            self.header = {}
            raw_header = raw_request.split('\r\n\r\n', 1)[0].split('\r\n')[1:]
            log('raw_header: ', raw_header)
            for lines in raw_header:
                k, v = lines.split(': ', 1)
                self.header[k] = v
            self.cookies = {}
            self.add_cookies()

    def add_cookies(self):
        raw_cookies = self.header.get('Cookie', None)
        if raw_cookies is not None:
            list_cookies = raw_cookies.split('; ', 1)
            log('原始cookie: ', raw_cookies)
            for line in list_cookies:
                if '=' in line:
                    k, v = line.split('=', 1)
                    self.cookies[k] = v
            log('字典cookie: ', self.cookies)
        else:
            log('请求中没有cookies')


request = Request()


def error(request, code=404):
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>404 NOT FOUND PAGE</h1>'
    }

    return e.get(code, b'')


def parse_path(path):
    index = path.find('?')

    if index == -1:
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        args = query_string.split("&")
        query = {}

        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


def response_for_path(path):
    path, query = parse_path(path)
    request.path = path
    request.query = query
    log('path and query', path, query)

    r = {
        '/static': route_static,
    }
    r.update(route_dict)
    r.update(todo_route)
    r.update(weibo_route)
    response = r.get(path, error)
    return response(request)


"""
def all_request_data(connect):
    buffer_size = 1024
    all_data = ''
    
    while True:
        single_request = connect.recv(buffer_size).decode('utf-8')
        if len(single_request) == 0:
            break
        all_data += single_request
    
    return all_data
"""


def run(host='', port=3000):

    log('start at', host, port)
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(5)
            connection, address = s.accept()
            r = connection.recv(1024).decode('utf-8')
            log("原始请求：", r)
            request.add_headers(r)
            log("字典化请求头：", request.header)
            if len(r.split()) < 2:
                continue   

            path = r.split()[1]
            request.method = r.split()[0]
            request.body = r.split('\r\n\r\n', 1)[1]
            response = response_for_path(path)
            connection.sendall(response)
            connection.close()


if __name__ == '__main__':
    config = {
        'host': '',
        'port': 3000,
    }
    run(**config)

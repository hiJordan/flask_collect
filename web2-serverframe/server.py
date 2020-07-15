import socket


def route_index():
    header = 'HTTP/1.1 2OO OK\r\ncontent-type:text/html\r\n\r\n'
    body = '<h1>Hello World</h1><img src="/doge.gif">'
    response = header + body

    return response.encode('utf-8')


def route_img():
    with open('doge.gif', 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\ncontent-type:image/gif\r\n\r\n'
        response = header + f.read()
        return response


def page(name):
    with open(name, encoding='utf-8') as f:
        return f.read()


def route_msg():
    header = 'HTTP/1.1 200 OK\r\ncontent-type:text/html\r\n\r\n'
    body = page('html_basic.html')
    response = header + body

    return response.encode('utf-8')


def error(code=404):
    e = {
        404: 'HTTP/1.1 404 NOT FOUND\r\ncontent-type:text/html\r\n\r\n<h1>404 NOT FOUND</h1>'
    }

    return e.get(code, b'').encode('utf-8')


def log(*args, **kwargs):
    print('log: ', *args, **kwargs)


def response_for_path(path):
    r = {
        '/': route_index,
        '/doge.gif': route_img,
        '/msg': route_msg,
    }
    response = r.get(path, error)

    return response()


def run(host='', port=3000):
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(5)
            connection, address = s.accept()
            request = connection.recv(1024).decode('utf-8')
            log('raw:', request)
            try:
                path = request.split()[1]
                response = response_for_path(path)
                connection.sendall(response)
            except Exception as e:
                log('error', e)
            connection.close()


def main():
    config = dict(
        host='',
        port=3000,
    )
    run(**config)


if __name__ == '__main__':
    main()
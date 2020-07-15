import socket
import ssl
import time


def log(*args, **kwargs):
    print('log: ', *args, **kwargs)


def parse_url(url):
    # 提取协议与uri
    protocol = url.split('://')[0]
    if protocol == 'http':
        protocol = 'http'
        uri = url.split('://')[1]
    elif protocol == 'https':
        protocol = 'https'
        uri = url.split('://')[1]
    else:
        uri = url

    # 提取主机地址
    index = uri.find('/')
    if index == -1:
        host = uri
    else:
        host = uri.split('/')[0]

    # 提取端口号
    http_ports = {
        'http': 80,
        'https': 443,
    }
    if protocol in http_ports:
        port = http_ports[protocol]
    else:
        port = uri.split(':')[1]

    # 提取路径
    if index == -1:
        path = '/'
    else:
        path = '/' + uri.split('/')[1]

    return protocol, host, port, path


def socket_by_protocol(protocol):
    if protocol == 'http':
        s = socket.socket()
    elif protocol == 'https':
        s = ssl.wrap_socket(socket.socket())

    return s


def response_by_socket(s):
    buffer_size = 1024
    all_data = b''

    while True:
        response = s.recv(buffer_size)
        if len(response) == 0:
            break
        all_data += response
    return all_data.decode()


def parse_response(response):
    errors = ''
    if response:
        header, body = response.split('\r\n\r\n', 1)
        header_line = header.split('\r\n')
        status_code = header_line[0].split()[1]
        headers = {}
        for line in header_line[1:]:
            k, v = line.split(': ')
            headers[k] = v
    else:
        errors = 'response is null value.'
        headers = {}
        body = ''

    return status_code, headers, body


def construct_request(host, path):
    request = 'GET {} HTTP/1.1\r\nhost: {}\r\nconnection: close\r\n\r\n'.format(path, host)
    return request.encode()


def get(url, query):
    protocol, host, port, path = parse_url(url)
    s = socket_by_protocol(protocol)

    s.connect((host, port))
    cons_path = '{}?{}={}'.format(path, query[1], query[0])
    request = construct_request(host, cons_path)
    s.send(request)
    response = response_by_socket(s)
    status_code, header, body = parse_response(response)

    return status_code, header, body


def parse_page(source=''):
    mv_name = []
    mv_score = []
    mv_people = []
    mv_quot = []

    first_split = str(source.split('<ol class="grid_view">').pop(1))
    second_split = str(first_split.split('</ol>').pop(0))
    third_split = second_split.split('<div class="info">')
    del third_split[0]

    for line in third_split:
        line = line.split('</li>')
        del line[1]

        # 名称抽取
        raw_single_mv_name = line[0].split('</a>')[0].split('<span class="title">')[1]
        single_mv_name = raw_single_mv_name.split('</span>')[0]
        mv_name.append(single_mv_name)

        # 分数与评价人数抽取
        raw_single_mv_evaluate = line[0].split('<div class="star">')[1].split('</span>')
        single_mv_score = raw_single_mv_evaluate[1].split('">')[1]
        mv_score.append(single_mv_score)
        single_mv_people = raw_single_mv_evaluate[3].split('<span>')[1]
        mv_people.append(single_mv_people)

        # 引用语抽取
        # log(mv_name, mv_score, mv_people, line[0])
       # log(line[0].split('<span class="inq">')[1])
        raw_singe_mv_quot = line[0].split('<span class="inq">')[1]
       # log(raw_singe_mv_quot)
        single_mv_quot = raw_singe_mv_quot.split('</span>')[0]
        #log(single_mv_quot)
        mv_quot.append(single_mv_quot)
        # 此处mv_quot有值
        log(mv_quot)
    #为何这里mv_quot提示list index out of range
    log(mv_quot)
    # log(len(mv_name), len(mv_score), len(mv_people), len(mv_quot))
    return mv_name, mv_score, mv_people, mv_quot


def main():
    url = "https://movie.douban.com/top250"
    protocol, host, port, path = parse_url(url)
    log(protocol, host, port, path)

    queries = {}
    for v in [value for value in range(250, 0, -25)]:
        queries[v] = 'start'

    log(queries)
    i = 0
    for q in queries.items():
        try:
            status_code, header, body = get(url, q)
            """
            if i == 8:
                log(status_code, header, body)
            """
            mvo_name, mvo_score, mvo_people, mvo_quot = parse_page(source=body)
           # log(mvo_name)
           # log(mvo_score)
           # log(mvo_people)
            log(mvo_quot)
            i += 1
        except Exception as e:
            log(e)
            continue


if __name__ == '__main__':
    main()

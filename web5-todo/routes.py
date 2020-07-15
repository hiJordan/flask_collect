from utils import log
import random
from models.user import User
from models.message import Message


msg_list = []
session = {}


def template(name):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def response_with_headers(header, code=200):
    headers = 'HTTP/1.1 {} OK\r\n'.format(code)
    headers += ''.join(['{}: {}\r\n'.format(k, v) for k, v in header.items()])
    return headers


def random_str():
    seed = 'ls-i@!qo13sii^+o2&sjo*a901ohj:so3ie:)!iow'
    s = ''
    for i in range(18):
        seed_index = random.randint(0, len(seed)-1)
        s += seed[seed_index]
    return s


def redirect(url):
    header = {
        'Location': url,
    }
    response = response_with_headers(header, code=302) + '\r\n'
    return response.encode('utf-8')


def current_user(request):
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '游客')
    return username


def route_index(request):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
    body = template('index.html')
    response = header + body
    return response.encode('utf-8')


def route_login(request):
    header = {
        'Content-Type': 'text/html',
    }
    username = current_user(request)
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            session_id = random_str()
            session[session_id] = u.username
            header['set-cookie'] = 'user={}'.format(session_id)
            result = '登录成功'
        else:
            result = '用户名或密码错误'
    else:
        result = ''
    body = template('login.html')
    log('first: ', body)
    body = body.replace('{{username}}', username)
    body = body.replace('{{result}}', result)
    headers = response_with_headers(header)
    response = headers + '\r\n' + body
    log('响应： ', response)
    return response.encode('utf-8')


def route_register(request):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format([str(u)+'<br>' for u in User.all()])
        else:
            result = '长度小于2'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    response = header + body
    return response.encode('utf-8')


def route_message(request):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'

    username = current_user(request)
    if username == '游客':
        return redirect('/')

    if request.method == 'POST':
        form = request.form()
        msg = Message.new(form)
        msg_list.append(msg)
    body = template('html_basic.html')
    msgs = '<br>'.join([str(m) for m in msg_list])
    body = body.replace('{{messages}}', msgs)
    response = header + body

    return response.encode('utf-8')


def route_static(request):
    header = b'HTTP/1.1 210 OK\r\nContent-Type: image/gif\r\n\r\n'
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        img = header + f.read()
        return img


route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    '/messages': route_message,
}


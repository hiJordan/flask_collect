from utils import log
from routes import current_user
from models.user import User
from models.todo import Todo
import time


def template(name):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def response_with_headers(header, code=200):
    headers = 'HTTP/1.1 {} OK\r\n'.format(code)
    headers += ''.join(['{}: {}\r\n'.format(k, v) for k, v in header.items()])
    return headers


def redirect(url):
    header = {
        'Location': url,
    }
    response = response_with_headers(header, code=302) + '\r\n'
    return response.encode('utf-8')


# func(request)相当于将被包装的函数加入wrap_func中,return warp_func返回包装后的函数对象。_
def login_required(func):
    def wrap_func(request):
        uname = current_user(request)
        user = User.find_by(username=uname)
        if user is None:
            return redirect('/login')

        return func(request)

    return wrap_func


def index(request):
    headers = {
        'Content-Type': 'text/html'
    }

    uname = current_user(request)
    user = User.find_by(username=uname)

    todo_lists = Todo.find_all(user_id=user.id)
    log('todo lists: ', todo_lists)
    todos = []
    for todo in todo_lists:
        edit_link = '<a href="/todo/edit?id={}">Edit</a>'.format(todo.id)
        delete_link = '<a href="/todo/delete?id={}">Remove</a>'.format(todo.id)
        created_time = time.strftime('%m/%d %H:%M', time.localtime(todo.create_time))
        updated_time = time.strftime('%m/%d %H:%M', time.localtime(todo.update_time))
        time_sch = '<sup><small>create by {}  update by {}</small></sup>'.format(created_time, updated_time)
        t = '<h3>{} : {} {} {} </h3>{}'.format(todo.id, todo.title, edit_link, delete_link, time_sch)
        todos.append(t)
    todo_html = ''.join(todos)
    header = response_with_headers(headers, code=200)
    body = template('todo_index.html')
    body = body.replace('{{todos}}', todo_html)
    response = header + '\r\n' + body
    log('todo response: ', response)
    return response.encode('utf-8')


def add(request):
    uname = current_user(request)
    user = User.find_by(username=uname)
    if request.method == 'POST':
        form = request.form()
        t = Todo.new(form)
        t.user_id = user.id
        t.create_time = time.time()
        log('add date:', t)
        t.save()
    return redirect('/todo')


def edit(request):
    headers = {
        'Content-Type': 'text/html'
    }
    uname = current_user(request)
    user = User.find_by(username=uname)
    todo = Todo.find_by(id=int(request.query.get('id', -1)))
    log('todo: ', todo, todo.user_id)
    if user.id != todo.user_id:
        return redirect('/todo')
    header = response_with_headers(headers)
    body = template('todo_edit.html')
    body = body.replace('{{todo_id}}', str(todo.id)).replace('{{todo_title}}', str(todo.title))
    response = header + '\r\n' + body

    return response.encode('utf-8')


def route_delete(request):
    uname = current_user(request)
    user = User.find_by(username=uname)
    todo = Todo.find_by(id=int(request.query.get('id', -1)))
    if todo.user_id != user.id:
        return redirect('/todo')
    if todo is not None:
        todo.remove()
    return redirect('/todo')


def update(request):
    uname = current_user(request)
    user = User.find_by(username=uname)
    if request.method == 'POST':
        form = request.form()
        todo = Todo.find_by(id=int(form.get('id', -1)))
        if todo.user_id != user.id:
            return redirect('/todo')
        todo.title = form.get('title', todo.title)
        todo.update_time = time.time()
        log('update data :', todo)
        todo.save()
    return redirect('/todo')


def admin_user(request):
    headers = {
        'Content-Type': 'text/html'
    }
    uname = current_user(request)
    user = User.find_by(username=uname)
    flashed = ''
    if user.role != 1:
        return redirect('/login')

    if request.method == 'POST':
        form = request.form()
        log('form :', form)
        user = User.find_by(id=int(form.get('id')))
        user.password = str(form.get('password'))
        if user.validate_register():
            user.save()
            return redirect('/admin/users')
        flashed = '密码长度需大于2'

    all_user_models = User.all()
    all_user_dict = [m.__dict__ for m in all_user_models]
    all_user = []
    for u in all_user_dict:
        user_line = '<h3>{} : {} {}</h3>'.format(u.get('id'), u.get('username'), u.get('password'))
        all_user.append(user_line)
    all_user_html = ''.join(all_user)
    header = response_with_headers(headers)
    body = template('users.html')
    body = body.replace('{{users}}', all_user_html)\
        .replace('{{user_id}}', str(user.id))\
        .replace('{{user_password}}', user.password)\
        .replace('{{flash}}', flashed)
    response = header + '\r\n' + body
    return response.encode('utf-8')


"""
def users_update(request):

    if request.method == 'POST':
        form = request.form()
        log('form :', form)
        user = User.find_by(id=int(form.get('id')))
        user.password = str(form.get('password'))
        if user.validate_register():
            user.save()
            return redirect('/admin/users')
        return redirect('/admin/users')
"""

route_dict = {
    '/todo': login_required(index),
    '/todo/add': login_required(add),
    '/todo/edit': login_required(edit),
    '/todo/update': login_required(update),
    '/todo/delete': login_required(route_delete),
    '/admin/users': login_required(admin_user),
    '/admin/users/update': login_required(admin_user),
}


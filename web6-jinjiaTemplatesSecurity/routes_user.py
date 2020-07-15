from utils import log
from utils import templates
from utils import redirect
from utils import http_response


import random
from models.user import User


session = {}


def random_str():
    seed = 'ls-i@!qo13sii^+o2&sjo*a901ohj:so3ie:)!iow'
    s = ''
    for i in range(18):
        seed_index = random.randint(0, len(seed)-1)
        s += seed[seed_index]
    return s


def current_user(request):
    session_id = request.cookies.get('user', '')
    user_id = int(session.get(session_id, '-1'))
    u = User.find_by(id=user_id)
    log('current_user: ', session_id, user_id, u)
    return u


def route_login(request):
    header = {}
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_login():
            user = User.find_by(username=u.username)
            session_id = random_str()
            session[session_id] = user.id
            header['set-cookie'] = 'user={}'.format(session_id)
            return redirect('/', headers=header)

    body = templates('login.html')
    return http_response(body)


def route_register(request):
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_register():
            u.save()
            return redirect('/login')
        else:
            return redirect('/register')

    body = templates('register.html')
    return http_response(body)


def admin_users(request):
    u = current_user(request)
    log('admin-users user data: ', u)
    if u is not None and u.is_admin():
        users = User.all()
        body = templates('users.html', users=users)
        return http_response(body)
    return redirect('/login')


def admin_users_update(request):
    form = request.form()
    user_id = int(form.get('id', -1))
    new_password = form.get('password', None)
    user = User.find_by(id=user_id)
    if user is not None:
        user.password = user.salted_password(new_password)
        user.save()
    return redirect('/admin/users')


route_dict = {
    '/login': route_login,
    '/register': route_register,
    '/admin/users': admin_users,
    '/admin/users/update': admin_users_update,
}


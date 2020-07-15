from utils import log
from utils import redirect
from utils import templates
from utils import http_response

from models.todo import Todo


def index(request):
    todo_list = Todo.all()
    body = templates('simple_todo_index.html', todos=todo_list)
    return http_response(body)


def add(request):
    form = request.form()
    Todo.new(form)
    return redirect('/')


def edit(request):
    todo = Todo.find_by(id=int(request.query.get('id')))
    log('edit todo :', todo)
    body = templates('simple_todo_edit.html', todo=todo)
    return http_response(body)


def todo_delete(request):
    todo = Todo.find_by(id=int(request.query.get('id')))
    todo.remove()
    return redirect('/')


def update(request):
    todo = Todo.find_by(id=int(request.query.get('id')))
    todo.task = request.form().get('task')
    todo.update_time = todo.ct()
    todo.save()
    return redirect('/')


route_dict = {
    '/': index,
    '/add': add,
    '/delete': todo_delete,
    '/edit': edit,
    '/update': update,
}


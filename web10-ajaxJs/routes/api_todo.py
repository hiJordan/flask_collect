import json
from routes.session import session
from utils import (
    log,
    redirect,
    http_response,
    json_response,
)
from models.todo import Todo
from models.weibo import Weibo


def all_todo(request):
    todo_list = Todo.all()
    todos = [todo.json() for todo in todo_list]
    return json_response(todos)


def add(request):
    form = request.json()
    todo = Todo.new(form)
    return json_response(todo.json())


def remove(request):
    todo_id = int(request.query.get('id'))
    todo = Todo.remove(todo_id)
    return json_response(todo.json())


def update(request):
    form = request.json()
    todo_id = int(form.get('id'))
    todo = Todo.update(todo_id, form)
    return json_response(todo.json())


route_dict = {
    '/api/todo/all': all_todo,
    '/api/todo/add': add,
    '/api/todo/delete': remove,
    '/api/todo/update': update,
}
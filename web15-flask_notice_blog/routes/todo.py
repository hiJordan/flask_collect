from flask import (
    Flask,
    request,
    redirect,
    url_for,
    Blueprint,
    render_template,
)
from models.todo import Todo
from utils import log


main = Blueprint('todo', __name__)


@main.route('/')
def index():
    todo_list = Todo.all()
    return render_template('todo_index.html', todos=todo_list)


@main.route('/add', methods=['post'])
def add():
    form = request.form
    m = Todo.new(form)
    return redirect(url_for('todo.index'))


@main.route('/delete/<int:todo_id>/')
def delete(todo_id):
    log('delete request method: ', request.method)
    m = Todo.delete(todo_id)
    return redirect(url_for('todo.index'))

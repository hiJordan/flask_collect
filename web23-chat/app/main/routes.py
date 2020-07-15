from flask import (
    session,
    redirect,
    url_for,
    render_template,
    request,
)
from . import bp_main


@bp_main.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if request.form.get('name') is not None:
            session['name'] = request.form.get('name')
            return redirect(url_for('.chat'))
    elif request.method == 'GET':
        return render_template('index.html')


@bp_main.route('/chat')
def chat():
    name = session.get('name', '')
    if name == '':
        return redirect(url_for('.index'))
    return render_template('chat.html')

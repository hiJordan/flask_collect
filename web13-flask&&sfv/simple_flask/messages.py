from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
)
import time

app = Flask(__name__)
msg_list = []


def log(*args, **kwargs):
    date_format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(date_format, value)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


@app.route('/')
def index():
    return 'this index page'


@app.route('/msg')
def msg():
    log('request method: ', request.method)
    log('request query ars: ', request.args)
    return render_template('msg_index.html', msg_list=msg_list)


@app.route('/msg/add', methods=['post'])
def msg_add():
    log('request method: ', request.method)
    log('request form: ', request.form)
    msg = dict(content=request.form.get('message_add', ''))
    msg_list.append(msg)
    return redirect(url_for('msg'))


if __name__ == "__main__":
    config = dict(
        debug=True,
        port=3000,
    )
    app.run(**config)
from flask import (
    Flask,
    redirect,
    render_template,
    url_for,
    Blueprint,
    request,
)
import time
from models.notice import Notice

bp_notice = Blueprint('notice', __name__)


@bp_notice.route('/')
def index():
    comments = Notice.all()
    return render_template('notice_index.html', comments=comments)


@bp_notice.route('/add', methods=['post'])
def add():
    form = request.form
    Notice.new(form)
    return redirect(url_for('.index'))

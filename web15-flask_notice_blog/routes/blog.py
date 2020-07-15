from flask import (
    request,
    redirect,
    render_template,
    Blueprint,
    url_for,
)
from models.blog import Blog, BlogComment

"""
    1.切分页面
        index--add元素、显示已存的blog条目
        add_blog--标题、内容、作者、创建时间
        view_blog--展示详细内容、评论信息、添加评论
    2.组织数据
        2.1 blog类
            数据--id、标题、内容、作者、创建时间
            方法--new、find_blog_id
        2.2 blogComment类
            数据--id、内容、作者、创建时间、所属blog_id
            方法--new、find_blog_id_comment
    3.逻辑
        当点击add blog则跳转到add_blog页，若有blog条目存在则将所有Blog的title显示，其条目点击可定向到对应的详情页
        add_blog页数据提交后，重定向到index_blog页
        在view_blog详情页显示对应的blog所有数据，评论提交后，再次重定向到此页
        
"""

bp_blog = Blueprint('blog', __name__)


@bp_blog.route('/')
def index():
    blogs = Blog.all()
    return render_template('index_blog.html', blogs=blogs)


@bp_blog.route('/add', methods=['post'])
def add():
    form = request.form
    Blog.new(form)
    return redirect(url_for(".index"))


@bp_blog.route('/new_blog')
def new_blog():
    return render_template('add_blog.html')


@bp_blog.route('/<int:blog_id>')
def view_blog(blog_id):
    blog = Blog.find(blog_id)
    comments = BlogComment.find_all(blog_id=blog_id)
    return render_template('view_blog.html', blog=blog, comments=comments)


@bp_blog.route('/add_comment', methods=['post'])
def add_comment():
    form = request.form
    c = BlogComment.new(form)
    return redirect(url_for('.view_blog', blog_id=c.blog_id))

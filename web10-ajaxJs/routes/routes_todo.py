from utils import redirect
from utils import templates
from utils import http_response


def main_index(request):
    return redirect('/todo/index')


def index(request):
    body = templates('todo_index.html')
    return http_response(body)


route_dict = {
    '/': main_index,
    '/todo/index': index,
}


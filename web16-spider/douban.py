import requests
import os
from pyquery import PyQuery as pq


class Model(object):
    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}: ({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n {}>'.format(name, '\n '.join(properties))
        return s


class Movie(Model):
    def __init__(self):
        self.name = ''
        self.score = 0
        self.quote = ''
        self.cover_url = ''
        self.ranking = 0


# def resource_exists(path):
#     folder, filename = os.path.split(path)
#     filename, file_ext = os.path.splitext(filename)
#
#     if os.path.exists(path) and file_ext == '.html':
#         with open(path, 'rb') as f:
#             return f.read()
#     elif os.path.exists(folder):
#         os.makedirs(folder)
#     else:
#         if not os.path.exists(folder):
#             os.makedirs(folder)


def cached_url(url):
    folder = 'cached'
    filename = url.split('=', 1)[-1] + '.html'
    path = os.path.join(folder, filename)

    if os.path.exists(path):
        with open(path, 'rb') as f:
            return f.read()
    else:
        if not os.path.exists(folder):
            os.makedirs(folder)
        headers = {
                    'user-agent': """Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
                                    (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36""",
                  }
        r = requests.get(url, headers=headers)
        with open(path, 'wb') as f:
            f.write(r.content)
        return r.content


def movie_for_url(div):
    e = pq(div)
    m = Movie()
    m.name = e('.title').text()
    m.score = e('.rating_num').text()
    m.quote = e('.quote').text()
    m.cover_url = e('img').attr('src')
    m.ranking = e('.pic').find('em').text()
    return m


def movies_for_url(url):
    page = cached_url(url)
    e = pq(page)
    items = e('.item')
    movies = [movie_for_url(item) for item in items]
    return movies


def download_img(url):
    folder = 'img'
    filename = url.split('/')[-1]
    path = os.path.join(folder, filename)

    if not os.path.exists(folder):
        os.makedirs(folder)
    if os.path.exists(path):
        return
    headers = {
        'user-agent': """Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
                        (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36""",
    }
    r = requests.get(url, headers=headers)
    with open(path, 'wb') as f:
        f.write(r.content)
    print('{} written successfully'.format(filename))


def main():
    for i in range(0, 250, 25):
        url = 'https://movie.douban.com/top250?start={}'.format(i)
        movies = movies_for_url(url)
        print('movies info: \n', movies)
        [download_img(movie.cover_url) for movie in movies]


if __name__ == "__main__":
    main()
from dataclasses import asdict, dataclass, field
from os import makedirs
from os.path import join as path_join

from blog.jinja_render import jinja_render
from blog.post import Post

@dataclass(init=False)
class Index:
    description: str
    title: str = None
    path: str = '/'
    posts: list[Post] = field(default_factory=list)

    def __init__(self, description, posts, path=None, title=None):
        self.description = description
        self.posts = sorted(
            posts,
            key=lambda p:(p.date, p.order),
            reverse=True
        )
        self.path = path
        self.title = title

    def write_files(self, dst):
        makedirs(dst, exist_ok=True)
        content_html = jinja_render('list', **asdict(self))
        with open(path_join(dst, 'content.html'), 'w') as f:
            f.write(content_html)

        me = asdict(self)
        me['content'] = content_html
        index_html = jinja_render('base', **me)
        with open(path_join(dst, 'index.html'), 'w') as f:
            f.write(index_html)


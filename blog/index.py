from dataclasses import asdict, dataclass, field
from math import ceil
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
    ENTRIES_PER_PAGE: int = 5

    def __init__(self, description, posts, path=None, title=None):
        self.description = description
        self.posts = sorted(
            posts,
            key=lambda p:(p.date, p.order),
            reverse=True
        )
        self.path = path.replace(' ', '-')
        self.title = title

    def write_page(self, page_num, num_pages, posts, dst, links):
        links_html = ''
        if len(links) > 1:
            links = [dict(it) for it in links]
            links[page_num]['active'] = False
            links_html = jinja_render('links', links=links)

        me = asdict(self)
        me['posts'] = posts
        me['links_html'] = links_html
        if num_pages > 1:
            me['path'] = f'{me["path"]}/{page_num+1}'
        content_html = jinja_render('list', **me)
        with open(path_join(dst, 'content.html'), 'w') as f:
            f.write(content_html)

        me['content'] = content_html
        index_html = jinja_render('base', **me)
        with open(path_join(dst, 'index.html'), 'w') as f:
            f.write(index_html)

    def write_files(self, dst):
        makedirs(dst, exist_ok=True)
        dst.replace(' ', '-')
        me = asdict(self)
        posts = me['posts']
        num_pages = ceil(len(posts) / self.ENTRIES_PER_PAGE)
        links = [{'endpoint':self.path.replace('//','/'), 'label':'1', 'active': True}]

        for page_num in range(1, num_pages):
            links += [{
                'endpoint': '/'.join((self.path, str(page_num+1))).replace('//','/'),
                'label': str(page_num+1),
                'active': True
            }]

        assert len(links) == num_pages

        for page_num in range(num_pages):
            page_idx = page_num * self.ENTRIES_PER_PAGE
            page_dst = dst
            if page_num != 0:
                page_dst = path_join(dst, str(page_num+1))
                page_dst = page_dst.replace(' ', '-')
                makedirs(page_dst, exist_ok=True)

            self.write_page(
                page_num,
                num_pages,
                self.posts[page_idx:page_idx+self.ENTRIES_PER_PAGE],
                page_dst,
                links
            )

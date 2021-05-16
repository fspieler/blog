from dataclasses import asdict, dataclass, field
from datetime import date
from os import makedirs
from os.path import basename, join as path_join

from blog.jinja_render import jinja_render
from blog.md_render import md_render

@dataclass
class Post:
    title: str
    endpoint: str
    order: int = -1
    date: date = None
    subtitle: str = ''
    display_date: str = ''
    tags: list[int] = field(default_factory=list)
    description: str = ''
    body: str = ''
    type: str = ''

    @classmethod
    def from_path(clz, path):
        endpoint = basename(path).split('.')[0]+'/'
        with open(path, 'r') as f:
            md_text = f.read()
        return clz.from_md(md_text, endpoint)

    @staticmethod
    def from_md(md_text, suggested_endpoint=''):
        args = md_render(md_text)
        if not 'endpoint' in args:
            args['endpoint'] = suggested_endpoint
        assert args['endpoint']
        args['tags'] = [it.strip() for it in args.get('tags', '').split(',') if it.strip()]
        if args.get('date'):
            args['date'] = date.fromisoformat(args['date'])
            args['display_date'] = args['date'].strftime('%A, %B %d, %Y').replace(' 0', ' ')
        return Post(**args)

    def write_files(self, dst, links=None):
        base = path_join(dst, self.endpoint)
        makedirs(base, exist_ok=True)
        me = asdict(self)
        if links:
            me['links'] = links
            me['links_html'] = jinja_render('links', **me)
        else:
            me['links_html'] = ''
        content_html = jinja_render('post', **me)
        with open(path_join(base, 'content.html'), 'w') as f:
            f.write(content_html)
        me['content'] = content_html
        index_html = jinja_render('base', **me)
        with open(path_join(base, 'index.html'), 'w') as f:
            f.write(index_html)

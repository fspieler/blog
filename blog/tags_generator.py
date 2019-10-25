from collections import defaultdict
import os

from jinja2 import Environment, PackageLoader, select_autoescape

from blog.page_converter import PageConverter

class Tag(object):
    def __init__(self):
        self.posts = []
    def append(self, **kwargs):
        self.posts.append(kwargs)
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return str(self.posts)

class TagsGenerator(object):
    def __init__(self):
        self.tags = defaultdict(Tag)
        self.jinja_environment = Environment(
            loader=PackageLoader('blog', 'templates'),
        )
        self.tag_template = self.jinja_environment.get_template('tag.html')
        self.page_template = self.jinja_environment.get_template('base.html')
    def __getitem__(self, tag):
        ret = self.tags[tag]
        ret.name = tag
        return ret
    def write_tags_pages(self):
        for tag, val in self.tags.items():
            tagdir = f'public/tag/{tag}'
            os.makedirs(tagdir, exist_ok=True)
            title = f'tag: {tag} - fredspieler.com'
            tag_html = self.tag_template.render(
                title=title,
                posts=val.posts
            )
            page_html = self.page_template.render(
                title=title,
                content=tag_html
            )
            with open(f'{tagdir}/content.html','w') as f:
                f.write(tag_html)
            with open(f'{tagdir}/index.html','w') as f:
                f.write(page_html)

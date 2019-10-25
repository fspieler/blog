import os
import errno

from markdown.extensions.attr_list import AttrListExtension
from markdown.extensions.def_list import DefListExtension
from markdown.extensions.fenced_code import CodeHiliteExtension, FencedCodeExtension
from markdown.extensions.meta import MetaExtension
from markdown.extensions.sane_lists import SaneListExtension
#from markdown.extensions.smart_strong import SmartEmphasisExtension
from markdown.extensions.smarty import SmartyExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension
from markdown.extensions.wikilinks import WikiLinkExtension
from markdown import Markdown
from mdx_linkify.mdx_linkify import LinkifyExtension

from jinja2 import Environment, PackageLoader, select_autoescape

class PageConverter(object):
    DEFAULT_EXTENSIONS = [
        AttrListExtension(),
        CodeHiliteExtension(),
        DefListExtension(),
        FencedCodeExtension(),
        MetaExtension(),
        SaneListExtension(),
#        SmartEmphasisExtension(),
        SmartyExtension(),
        TableExtension(),
        TocExtension(),
        WikiLinkExtension(),
        LinkifyExtension()
    ]

    def __init__(self, input_path, output_dir):
        self.input_path = input_path
        self.output_dir = output_dir
        self.md = Markdown(
            extensions=PageConverter.DEFAULT_EXTENSIONS
        )
        self.jinja_environment = Environment(
            loader=PackageLoader('blog', 'templates'),
        )
        self.post_template = self.jinja_environment.get_template('post.html')
        self.base_template = self.jinja_environment.get_template('base.html')

    def apply_template(self, **kwargs):
        pass

    @staticmethod
    def meta_list_convert(meta_dict):
        ret = {}
        for k, v in meta_dict.items():
            if isinstance(v, list):
                v = v[0]
            ret[k] = v
        return ret

    def _transform(self, md_text, output_path, permalink):
        md_html = self.md.convert(md_text)
        meta = self.meta_list_convert(self.md.Meta)
        print(meta)
        if output_path.startswith('public/'):
            output_path = output_path[7:]
        jinja_input = {
            'title' : meta['title'],
            'body' : md_html,
            'path' : output_path,
            'permalink' : permalink
        }
        if 'date' in meta:
            jinja_input['date'] = meta['date']
        if 'tags' in meta:
            jinja_input['tags'] = meta['tags'].split(', ')
        if 'subtitle' in meta:
            jinja_input['subtitle'] = meta['subtitle']
        content_html = self.post_template.render(**jinja_input)
        jinja_input['content'] = content_html
        full_page_html = self.base_template.render(jinja_input)
        return (content_html, full_page_html, meta)

    def convert(self, tags_generator=None, index_generator=None, permalink=True):
        with open(self.input_path, 'r') as f:
            input_md = f.read()
        file_base = os.path.basename(self.input_path).replace('.md','')
        output_path = f'{self.output_dir}/{file_base}'

        content_html, full_page_html, meta = self._transform(
            input_md,
            output_path,
            permalink
        )

        if tags_generator and 'tags' in meta:
            for tag in meta['tags'].split(', '):
                tags_generator[tag].append(
                    path=output_path,
                    meta=meta,
                    content=content_html
                )

        if index_generator:
            index_generator.append(
                meta=meta,
                path=output_path,
                content=content_html
            )

        os.makedirs(output_path, exist_ok=True)
        with open(f'{output_path}/content.html','w') as f:
            f.write(content_html)
        with open(f'{output_path}/index.html','w') as f:
            f.write(full_page_html)

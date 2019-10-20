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

    def _transform(self, md_text):
        md_html = self.md.convert(md_text)
        meta = self.md.Meta
        jinja_input = {
            'title' : meta['title'][0],
            'date' : meta['date'][0],
            'body' : md_html
        }
        if 'subtitle' in meta:
            jinja_input['subtitle'] = meta['subtitle'][0]
        content_html = self.post_template.render(**jinja_input)
        del jinja_input['body']
        jinja_input['title'] += ' - fredspieler.com'
        jinja_input['content'] = content_html
        full_page_html = self.base_template.render(jinja_input)
        return (content_html, full_page_html)

    def convert(self):
        with open(self.input_path, 'r') as f:
            input_md = f.read()
        content_html, full_page_html = self._transform(input_md)

        os.makedirs(os.path.dirname(self.output_dir), exist_ok=True)
        file_base = os.path.basename(self.input_path)
        output_path = f'{self.output_dir}/{file_base}'
        with open(f'{output_path}.raw.html','w') as f:
            f.write(content_html)
        with open(f'{output_path}.html','w') as f:
            f.write(full_page_html)




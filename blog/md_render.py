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
from mdx_oembed import OEmbedExtension
import oembed

def md_render(md_text) :
    md = Markdown(extensions=[
        AttrListExtension(),
        CodeHiliteExtension(guess_lang=False),
        DefListExtension(),
        FencedCodeExtension(),
        MetaExtension(),
        OEmbedExtension(allowed_endpoints={
            oembed.OEmbedEndpoint(
                'https:\/\/publish.twitter.com\/oembed',
                [
                    "https:\/\/twitter.com\/*\/status\/*",
                    "https:\/\/*.twitter.com\/*\/status\/*"
                ]
            )
        }),
        SaneListExtension(),
#        SmartEmphasisExtension(),
        SmartyExtension(),
        TableExtension(),
        TocExtension(),
        WikiLinkExtension(),
        LinkifyExtension()
    ])
    body = md.convert(md_text)
    ret = dict(meta_list_convert(md.Meta))
    ret['body'] = body
    return ret

def meta_list_convert(meta_dict):
    ret = {}
    for k, v in meta_dict.items():
        if isinstance(v, list):
            v = v[0]
        ret[k] = v
    return ret


import glob
import shutil
import os

from blog.page_converter import PageConverter
from blog.tags_generator import TagsGenerator
from blog.index_generator import IndexGenerator

def init_public():
    shutil.rmtree('public', ignore_errors=True)
    os.makedirs('public')

def copy_static():
    shutil.copytree('static/css','public/css')
    shutil.copytree('static/img','public/img')
    shutil.copytree('static/js','public/js')
    shutil.copy2('static/img/favicon.ico','public/favicon.ico')
    PageConverter('errors/404.md','public').convert(permalink=False)
    PageConverter('errors/50x.md','public').convert(permalink=False)

def generate_blog_content(tags_generator, index_generator):
    files = glob.glob('content/*.md')
    for f in files:
        PageConverter(f, 'public').convert(
            tags_generator=tags_generator,
            index_generator=index_generator
        )


def main():
    init_public()
    copy_static()

    tags_generator = TagsGenerator()
    index_generator = IndexGenerator()

    generate_blog_content(tags_generator, index_generator)
    index_generator.write_home_index()
    tags_generator.write_tags_pages()
    print(tags_generator.tags.keys())


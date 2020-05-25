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
    shutil.copy2('static/robots.txt', 'public/robots.txt')
    shutil.copy2('static/img/favicon.ico','public/favicon.ico')
    PageConverter('errors/404.md','public').parse(permalink=False).write()
    PageConverter('errors/50x.md','public').parse(permalink=False).write()

def generate_blog_content(tags_generator, index_generator):
    files = glob.glob('content/*.md')
    ret = []
    for f in files:
        ret.append(
            PageConverter(f, 'public').parse(
                tags_generator=tags_generator,
                index_generator=index_generator
            )
        )
    return ret


def main():
    init_public()
    copy_static()

    tags_generator = TagsGenerator()
    index_generator = IndexGenerator()

    posts = generate_blog_content(tags_generator, index_generator)
    index_generator.sort_posts()
    index_generator.write_home_index()
    index_generator.update_links()
    tags_generator.write_tags_pages()
    for post in posts:
        post.write()
    print(tags_generator.tags.keys())

if __name__ == '__main__':
    main()

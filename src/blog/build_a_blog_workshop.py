from collections import defaultdict
from glob import glob
from os import sep, makedirs
from os.path import join as path_join, exists
from shutil import copytree, rmtree

from blog.post import Post
from blog.index import Index

def create_raw_posts():
    posts = []
    tag_lookup = defaultdict(list)
    for f in glob(f'content{sep}*.md'):
        p = Post.from_path(f)
        posts.append(p)
        for tag in p.tags:
            tag_lookup[tag].append(p)
    return posts, tag_lookup

def main():
    dst = 'public'
    if exists(dst):
        rmtree(dst)
    copy_static(dst)
    makedirs(path_join(dst, 'tag'), exist_ok=True)
    posts, tag_lookup = create_raw_posts()
    for tag, tposts in tag_lookup.items():
        Index(
            posts=tposts,
            path=f'/tag/{tag}',
            title=f'tag: {tag}',
            description=f'tag: {tag}',
        ).write_files(path_join(dst, 'tag', tag.replace(' ', '-')))
    index = Index(
        posts=posts,
        description='your internet home for all things FredSpieler.com',
        path='/'
    )
    index.write_files(dst)
    posts = index.posts
    for idx, post in enumerate(posts):
        links = [{
            "active": post is not posts[0],
            "label": 'latest',
            "endpoint": '/'+posts[0].endpoint if post != posts[0] else '',
        },{
            "active": post is not posts[0],
            "label": 'next',
            "endpoint": '/'+posts[idx-1].endpoint if post != posts[0] else '',
        },{
            "active": post is not posts[-1],
            "label": 'previous',
            "endpoint": '/'+posts[idx+1].endpoint if post != posts[-1] else '',
        },{
            "active": post is not posts[-1],
            "label": 'oldest',
            "endpoint": '/'+posts[-1].endpoint if post != posts[-1] else '',
        }]
        post.write_files(dst, links)

def copy_static(dst='public'):
    copytree(
        'static',
        dst,
        ignore=lambda d, files: [f for f in files if f.startswith('.')],
    )
    for f in glob(f'content/errors{sep}*.md'):
        Post.from_path(f).write_files(dst)

if __name__ == '__main__':
    main()

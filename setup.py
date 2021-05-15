#!/usr/bin/env python3

from distutils.core import setup
setup(
    name='fred-spieler-blog',
    version='1.0',
    py_modules=['blog'],
    install_requires=[
        'jinja2',
        'livereload',
        'markdown',
        'mdx_linkify',
        'python-markdown-oembed',
    ],
    entry_points= {
        'console_scripts': [
            'build-a-blog=blog.build_a_blog_workshop:main',
            'dev_reload=dev_reload:dev_reload'
        ]
    }
)

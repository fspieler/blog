import shutil
import os

from blog.page_converter import PageConverter

def main():
    shutil.rmtree('public', ignore_errors=True)
    os.makedirs('public')
    shutil.copytree('static/css','public/css')
    shutil.copytree('static/img','public/img')
    shutil.copytree('static/js','public/js')
    PageConverter('content/i-dont-know-php.md', 'public/').convert()

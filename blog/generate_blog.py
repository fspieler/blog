import shutil
import os

from blog.page_converter import PageConverter



def main():
    shutil.rmtree('public', ignore_errors=True)
    os.makedirs('public')
    shutil.copytree('css','public/css')
    shutil.copytree('img','public/img')
    shutil.copytree('js','public/js')
    PageConverter('content/i-dont-know-php.md', 'public/').convert()

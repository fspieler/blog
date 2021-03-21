from os.path import exists
import shutil
import subprocess

from livereload import Server

def build():
    subprocess.run(['python', 'blog/build_a_blog_workshop.py'])

def dev_reload():
    path = 'public'
    if exists(path):
        shutil.rmtree(path)
    build()
    server = Server()
    server.watch('content/**', build)
    server.watch('static/**/*', build)
    server.watch('blog/**/*', build)
    server.watch('errors/**', build)
    server.watch('*', build)
    server.serve(
        root=path,
        host='0.0.0.0'
    )

if __name__ == '__main__':
    dev_reload()

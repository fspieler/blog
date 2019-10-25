from livereload import Server
from blog.generate_blog import main as regen

def main():
    server = Server()
    server.watch('content/**', regen)
    server.watch('static/**/*', regen)
    server.watch('blog/**/*', regen)
    server.watch('errors/**', regen)
    server.watch('*', regen)
    server.serve(
        root='public',
        port=8000,
        host='0.0.0.0'
    )

from livereload import Server
from blog.generate_blog import main

def dev_reload():
    server = Server()
    server.watch('content/**', main)
    server.watch('static/**/*', main)
    server.watch('blog/**/*', main)
    server.watch('errors/**', main)
    server.watch('*', main)
    server.serve(
        root='public',
        host='0.0.0.0'
    )

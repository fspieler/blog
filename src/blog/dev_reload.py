from os.path import exists
import shutil
import subprocess
import sys

from livereload import Server

def build():
    """run in a sub-process because we want to force reloading"""
    subprocess.run(["build-a-blog"])

def main():
    path = "public"
    if exists(path):
        shutil.rmtree(path)
    build()
    server = Server()
    server.watch("content/**", build)
    server.watch("static/**/*", build)
    server.watch("blog/**/*", build)
    server.watch("errors/**", build)
    server.watch("*", build)
    server.serve(
        root=path,
        host="0.0.0.0"
    )

if __name__ == "__main__":
    main()

import shutil
from blog.page_converter import PageConverter

class IndexGenerator(object):
    def __init__(self):
        self.posts = {}
        self.max = -1
    def append(self, **kwargs):
        order = int(kwargs['meta']['order'])
        self.posts[order] = kwargs
        self.max = max(self.max, order)
    def write_home_index(self):
        shutil.copy2(f'{self.posts[self.max]["path"]}/index.html', 'public/index.html')
        shutil.copy2(f'{self.posts[self.max]["path"]}/content.html', 'public/content.html')



import os
from blog.page_converter import PageConverter

class IndexGenerator(object):
    def __init__(self):
        self.posts = []
        self.max = -1
    def append(self, **kwargs):
        kwargs['meta']['order'] = int(kwargs['meta']['order'])
        self.posts.append(kwargs)
    def sort_posts(self):
        self.posts.sort(key=lambda x:x['meta']['order'], reverse=True)
    def write_home_index(self):
        os.symlink(f'{self.posts[0]["path"]}/index.html'.replace('public/',''), 'public/index.html')
        os.symlink(f'{self.posts[0]["path"]}/content.html'.replace('public/',''), 'public/content.html')

    def update_links(self):
        last_idx = len(self.posts)-1
        for idx, post in enumerate(self.posts):
            links = []
            if idx > 0:
                links.append({
                    'value': self.posts[0]['path'].replace('public',''),
                    'label': 'latest'
                })
                links.append({
                    'value': self.posts[idx-1]['path'].replace('public',''),
                    'label': 'next'
                })
            if idx < last_idx:
                links.append({
                    'value': self.posts[idx+1]['path'].replace('public',''),
                    'label': 'previous'
                })
                links.append({
                    'value': self.posts[last_idx]['path'].replace('public',''),
                    'label': 'oldest'
                })
            print(links)
            post['page_converter'].update_links(links)


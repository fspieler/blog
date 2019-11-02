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
                next_value = self.posts[idx-1]['path'].replace('public','')
            else:
                next_value = ''
            links.append({
                'value': self.posts[0]['path'].replace('public',''),
                'label': 'latest',
                'active': idx > 0
            })
            links.append({
                'value': next_value,
                'label': 'next',
                'active': idx > 0
            })
            if idx < last_idx:
                previous_value = self.posts[idx+1]['path'].replace('public','')
                oldest_value = self.posts[last_idx]['path'].replace('public','')
            else:
                previous_value = ''
                oldest_value = ''
            links.append({
                'value': previous_value,
                'label': 'previous',
                'active': idx < last_idx
            })
            links.append({
                'value': oldest_value,
                'label': 'oldest',
                'active': idx < last_idx

            })
            print(links)
            post['page_converter'].update_links(links)


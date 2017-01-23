import os

from phim.settings import BASE_DIR
from proxylist import ProxyList

class ProxyMiddleware(object):
    def __init__(self):
        self.pl = ProxyList()
        self.pl.load_file(os.path.join(BASE_DIR, 'proxy/proxylist.txt'))

    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://{}'.format(self.pl.random().address())

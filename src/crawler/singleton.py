import requests
from bs4 import BeautifulSoup


class Session_591():
    def __init__(self, region_code):
        self.token = None
        self.session = requests.session()
        self.region_code = region_code

    def update_token(self):
        self.session = requests.session()
        self.set_token(self.getCsrfToken())

    def getCsrfToken(self, url_591='https://rent.591.com.tw'):
        headers = {'User-Agent': 'Custom'}
        bs = BeautifulSoup(
            self.session.get(url_591,
                             headers=headers,
                             cookies={
                                 'urlJumpIp': str(self.region_code)
                             }).text, 'html.parser')
        tag = bs.html.head.find('meta', {'name': 'csrf-token'})
        token = tag.attrs['content']
        return token

    def set_token(self, token):
        self.token = token


session_591 = Session_591(1)

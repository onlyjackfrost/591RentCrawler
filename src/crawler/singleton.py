import requests
from bs4 import BeautifulSoup


class Session_591():
    def __init__(self):
        self.token = None
        self.session = requests.session()

    def update_token(self):
        self.session = requests.session()
        self.set_token(self.getCsrfToken())

    def getCsrfToken(self, url_591='https://rent.591.com.tw/?region=1'):
        headers = {'User-Agent': 'Custom'}
        bs = BeautifulSoup(
            self.session.get(url_591, headers=headers).text, 'html.parser')
        tag = bs.html.head.find('meta', {'name': 'csrf-token'})
        token = tag.attrs['content']
        return token

    def set_token(self, token):
        self.token = token


session_591 = Session_591()

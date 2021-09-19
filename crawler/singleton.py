import requests
from bs4 import BeautifulSoup


session = requests.session()

def getCsrfToken(url_591='https://rent.591.com.tw/'):
    bs = BeautifulSoup(
        session.get(url_591, cookies={
            'urlJumpIp': '1'
        }).text, 'html.parser')
    tag = bs.html.head.find('meta', {'name': 'csrf-token'})
    token = tag.attrs['content']
    return token

csrf_Token = getCsrfToken()  #global variable

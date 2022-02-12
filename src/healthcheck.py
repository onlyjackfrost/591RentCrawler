import requests


def selfHealthCheck():
    r = requests.get('https://intense-dawn-00035.herokuapp.com/')
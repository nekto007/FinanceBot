import requests
import settings
import sqlite3
from requests.auth import HTTPBasicAuth


def auth():
    response = requests.get(settings.MOEX_AUTH_URL, auth=HTTPBasicAuth(settings.EMAIL, settings.PASSWORD))
    return response.headers['X-Moex-Passport-Certificate']

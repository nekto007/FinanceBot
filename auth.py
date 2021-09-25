import requests
from requests import cookies
import settings
from requests.auth import HTTPBasicAuth

def auth():
    response = requests.get(settings.MOEX_AUTH_URL, auth=HTTPBasicAuth(settings.EMAIL, settings.PASSWORD))
    global validation_cookie
    validation_cookie = response.cookies
    current_cookie = response.cookies.get_dict()['MicexPassportCert']
    return current_cookie

def is_cookie_expired(cookie_for_check):
    for cookie in cookie_for_check:
        if cookie.is_expired()==True:
            auth()
        else:
            print('OK')


if __name__ == '__main__':
    pass
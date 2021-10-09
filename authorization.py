import requests
import settings
from requests.auth import HTTPBasicAuth


validation_cookie = ''


def get_auth():
    response = requests.get(settings.MOEX_AUTH_URL, auth=HTTPBasicAuth(settings.EMAIL, settings.PASSWORD))
    global validation_cookie #Глобальная переменная бъявления для доступа к куки из других функций (is_cookie_expired)
    validation_cookie = response.cookies
    current_cookie = response.cookies.get_dict()['MicexPassportCert']
    cookie_for_request = {'MicexPassportCert' : current_cookie} #словарь куки для передачи в запрос. Проверить(!)
    return cookie_for_request


def is_cookie_expired(cookie_for_check):
    for cookie in cookie_for_check:
        if cookie.is_expired():
            get_auth()
        else:
            print('Cookie is OK')


if __name__ == '__main__':
    pass

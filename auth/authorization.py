import requests
import settings
from requests.auth import HTTPBasicAuth

from datetime import datetime, timedelta
from db.db_connect import db_session
from models.db_models import Authorization

def get_auth():
    #db_cookie = db_session.query(Authorization, Authorization.token).filter(Authorization.is_expired == False)

    response = requests.get(settings.MOEX_AUTH_URL, auth=HTTPBasicAuth(settings.EMAIL, settings.PASSWORD))
    current_cookie = response.cookies.get_dict()['MicexPassportCert']
    cookie_for_request = {'MicexPassportCert' : current_cookie} #словарь куки для передачи в запрос. Проверить(!)
    print('RUN')

# def is_cookie_expired(cookie_for_check):
#     for cookie in cookie_for_check:
#         if cookie.is_expired():
#             get_auth()
#         else:
#             print('Cookie is OK')


# if __name__ == '__main__':
#     get_auth()
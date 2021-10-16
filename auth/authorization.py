import requests
from configs import settings
from requests.auth import HTTPBasicAuth
from db.db_connect import db_session
from models.db_models import Authorization

def get_auth():
    s = requests.Session()
    sign_up_request = s.get(settings.MOEX_AUTH_URL, auth=HTTPBasicAuth(settings.EMAIL, settings.PASSWORD))
    cookies = {'MicexPassportCert': s.cookies['MicexPassportCert']}
    token_to_db = Authorization(token=s.cookies['MicexPassportCert'])
    db_session.add(token_to_db)
    db_session.commit()
    cookie_last = db_session.query(Authorization).order_by(Authorization.id.desc()).limit(1)[::-1]
    #куки для запроса: {'MicexPassportCert': cookie_last}. Вынести в отдельную функцию для
    #вызова при запросах и передачи последних куки. Проверять header - если приходит Marker - denied -
    #пробовать авторизоваться и брать куки оттуда. Если продолжает приходить marker denied - продолжать дальше.
    print(sign_up_request.headers)

    return cookie_last

if __name__ == '__main__':
    get_auth()
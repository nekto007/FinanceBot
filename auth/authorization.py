import requests
from configs import settings
from requests.auth import HTTPBasicAuth
from db.db_connect import db_session
from db_models import Authorization

def get_auth():
    s = requests.Session()
    sign_up_request = s.get(settings.MOEX_AUTH_URL, auth=HTTPBasicAuth(settings.EMAIL, settings.PASSWORD))
    cookies = {'MicexPassportCert': s.cookies['MicexPassportCert']}
    token_to_db = Authorization(token=s.cookies['MicexPassportCert'])
    db_session.add(token_to_db)
    db_session.commit()
    cookie_last = {'MicexPassportCert':db_session.query(Authorization.token).order_by(Authorization.id.desc()).first()[0]}
    return cookie_last


if __name__ == '__main__':
    pass

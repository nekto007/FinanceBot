import requests
from configs import settings
from requests.auth import HTTPBasicAuth
from db.db_connect import db_session
from models.db_models import Authorization

def get_auth():
    s = requests.Session()
    s.get(settings.MOEX_AUTH_URL, auth=HTTPBasicAuth(settings.EMAIL, settings.PASSWORD))
    headers = {}
    cookies = {'MicexPassportCert': s.cookies['MicexPassportCert']}
    url = 'http://iss.moex.com/iss/engines.xml'
    req = requests.get(url, headers=headers, cookies=cookies)

    token_to_db = Authorization(token=s.cookies['MicexPassportCert'])
    db_session.add(token_to_db)
    db_session.commit()

    print(f"X-MicexPassport-Marker: {req.headers['X-MicexPassport-Marker']}; Expires: {req.headers['expires']}")

if __name__ == '__main__':
    get_auth()
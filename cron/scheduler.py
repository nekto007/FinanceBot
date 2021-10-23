import time
from datetime import datetime

import schedule

from api.moex.price import get_price
from db.db_connect import db_session
from models.db_models import (
    Calendar,
)


def job():
    calendar = db_session.query(Calendar.date).all()
    alert_list = db_session.query(Calendar.date).all()
    if datetime.now().date() in calendar:
        print(get_price('sber'.upper()))
    else:
        print('Пей пиво, к черту акции')


schedule.every(5).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

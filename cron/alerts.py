from datetime import datetime

from db.db_connect import db_session
from db_models import (
    Cron,
)


def create_alert(emitet, cost, chat_id):
    print(emitet, chat_id)
    print(cost)
    alert_list = db_session.query(Cron.sec_id) \
        .filter(Cron.cron_status == 1, Cron.chat_id == chat_id, Cron.sec_id == emitet, Cron.sum == cost
                , Cron.cron_type == 'alert').all()
    print(alert_list)
    if alert_list:
        return True
    else:
        add_alert = Cron(
            chat_id=chat_id,
            sec_id=emitet.upper(),
            sum=int(cost)*100,
            cron_type='alert',
            created_at=datetime.now(),
            updated_at=datetime.now())
        print(alert_list)
        db_session.add(add_alert)
        db_session.commit()
        return True


def remove_alert(emitet, chat_id):
    alert_list = db_session.query(Cron.sec_id) \
        .filter(Cron.cron_status == 1, Cron.chat_id == chat_id, Cron.sec_id == emitet).all()
    if alert_list:
        disable_cron = {'cron_status': False}
        db_session.query(Cron).filter_by(sec_id=emitet, chat_id=chat_id, cron_type='alert').update(disable_cron)
        db_session.commit()
        return len(alert_list)
    else:
        return len(alert_list)


def list_alert(chat_id):
    print('emitet, chat_id', chat_id)
    alert_list = db_session.query(Cron.sec_id, Cron.sum) \
        .filter(Cron.cron_status == 1, Cron.chat_id == chat_id, Cron.cron_type == 'alert').all()
    if alert_list:
        return alert_list


if __name__ == '__main__':
    print(list_alert('6885580'))
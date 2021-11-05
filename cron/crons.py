from datetime import datetime

from db.db_connect import db_session
from db_models import (
    Cron,
)


def create_cron(emitet, chat_id, cron_type, cost=0):
    print(emitet, chat_id)
    print(cost)
    if cost:
        cron_list = db_session.query(Cron.sec_id) \
            .filter(Cron.cron_status == 1, Cron.chat_id == chat_id, Cron.sec_id == emitet.upper(), Cron.sum == cost
                    , Cron.cron_type == cron_type).all()
    else:
        cron_list = db_session.query(Cron.sec_id) \
            .filter(Cron.cron_status == 1, Cron.chat_id == chat_id, Cron.sec_id == emitet.upper(),
                    Cron.cron_type == cron_type).all()
    if cron_list:
        return True
    else:
        add_cron = Cron(
            chat_id=chat_id,
            sec_id=emitet.upper(),
            sum=float(cost)*100,
            cron_type=cron_type,
            created_at=datetime.now(),
            updated_at=datetime.now())
        db_session.add(add_cron)
        db_session.commit()
        return True


def remove_cron(emitet, chat_id, cron_type):
    cron_list = db_session.query(Cron.sec_id) \
        .filter(Cron.cron_status == 1, Cron.chat_id == chat_id, Cron.sec_id == emitet, Cron.cron_type == cron_type)\
        .all()
    if cron_list:
        disable_cron = {'cron_status': False}
        db_session.query(Cron).filter_by(sec_id=emitet, chat_id=chat_id, cron_type=cron_type).update(disable_cron)
        db_session.commit()
        return len(cron_list)
    else:
        return len(cron_list)


def list_cron(chat_id, cron_type):
    cron_list = db_session.query(Cron.sec_id, Cron.sum) \
        .filter(Cron.cron_status == 1, Cron.chat_id == chat_id, Cron.cron_type == cron_type).all()
    if cron_list:
        return cron_list


if __name__ == '__main__':
    pass
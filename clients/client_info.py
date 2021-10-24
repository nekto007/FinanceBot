from db.db_connect import db_session
from models.db_models import Clients


def client_info(update, context):
    client_data = update.message.chat
    client = Clients(telegram_id=client_data['id'],
                     first_name=client_data['first_name'],
                     last_name=client_data['last_name'],
                     username=client_data['username'],
                     message=update.message.text)
    db_session.add(client)
    try:
        db_session.commit()
    except:
        db_session.rollback()
        # ignore error
        pass


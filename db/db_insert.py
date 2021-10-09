from db_connect import db_session
from models.db_models import Authorization


current_token = Authorization(token = 'test2')
db_session.add(current_token)
db_session.commit()

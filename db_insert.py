from db_connect import db_session
from db_models import Authorization


current_token = Authorization(token = 'test1')
db_session.add(current_token)
db_session.commit()
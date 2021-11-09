import requests
from datetime import datetime, timedelta
from db.db_connect import db_session
from db_models import Currency
from clients.client_info import post_client_info
from sqlalchemy.exc import IntegrityError


def get_currency_api():
    curr_date = db_session.query(Currency.updated_at).order_by(Currency.updated_at.desc()).first()
    diff_time = datetime.now() - curr_date[0]
    if diff_time > timedelta(minutes=15):
        print('DIFFTIME > TIMEDELTA')
        currency_info = {}
        url = 'https://iss.moex.com/iss/statistics/engines/futures/markets/indicativerates/securities.json?iss.meta=off'
        response = requests.get(url)
        currency_data = response.json()['securities']['data']
        for _x in currency_data:
            currency_info[_x[2]] = _x[3]
            currency_to_db = Currency(sec_id=_x[2], value=_x[3], created_at=datetime.now(), updated_at=datetime.now())
            db_session.add(currency_to_db)
            try:
                db_session.commit()
            except IntegrityError:
                db_session.rollback()
            db_session.close()
        return currency_info
    else:
        print('FROM DB')
        currency_info={}
        request_to_db=db_session.query(Currency.sec_id, Currency.value).order_by(Currency.updated_at.desc()).limit(18)
        for _y in request_to_db:
            currency_info[_y[0]]=_y[1]
        return currency_info


def get_all_currency(update, context):
    post_client_info(update, '')
    currency_array = get_currency_api()
    print(currency_array['USD/RUB'], currency_array['EUR/RUB'])
    update.message.reply_text(
        f'<b>Текущая дата: {datetime.now().date()}\n'
        f"Текущая котировка USD/RUB : {currency_array['USD/RUB']}\n"
        f"Текущая котировка EUR/RUB : {currency_array['EUR/RUB']}</b>\n",
        parse_mode='HTML')


def rub(update, context):
    currency_info = get_currency_api()
    text = update.message.text.split()
    value = float(text[1])
    return update.message.reply_text(f"USD : {round(value/currency_info['USD/RUB'],2)}, "
                                     f"EUR : {round(value/currency_info['EUR/RUB'],2)}")


def usd(update, context):
    currency_info = get_currency_api()
    text = update.message.text.split()
    value = float(text[1])
    return update.message.reply_text(f"RUB : {round(value*currency_info['USD/RUB'],2)}")


def eur(update, context):
    currency_info = get_currency_api()
    text = update.message.text.split()
    value = float(text[1])
    return update.message.reply_text(f"RUB : {round(value*currency_info['EUR/RUB'],2)}")


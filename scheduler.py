import os
import time
import logging
from datetime import datetime
from sqlalchemy import desc
import schedule
import telegram
from cron.crons import remove_cron
from telegram.error import Unauthorized
from api.moex.price import (
    get_stock_history_previous_day
)
from configs import settings
from db.db_connect import db_session
from db_models import (
    Calendar,
    Cron,
)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def job():
    bot = telegram.Bot(settings.BOT_API_KEY)
    subscribes_list = db_session.query(Cron.sec_id, Cron.chat_id) \
        .filter(Cron.cron_status == 1, Cron.cron_type == 'notification').all()
    if subscribes_list:
        previous_working_day = db_session.query(Calendar.date).filter(Calendar.date < str(datetime.now().date())) \
            .order_by(desc(Calendar.date)).limit(15).first()[0]
        f'<b>Текущая дата: {datetime.now().date()}\n'
        f'Здравствуйте!\n Вы получили это сообщение, т.к. подписались на автоматическую рассылку обновлений!'
        for subscribe in subscribes_list:
            emitet, chat_id = subscribe
            history_info = get_stock_history_previous_day(emitet, previous_working_day)
            short_name, sec_id, open_cost, close_cost, value_trade, number_of_trades, low_cost, high_cost, trade_date \
                = history_info[0]
            photo = history_info[1]
            try:
                bot.sendMessage(chat_id,
                                f'<b>Наименование компании: {short_name}\n'
                                f'Наименование тикета: {sec_id} \n'
                                f'Цена открытия: {open_cost / 100} \n'
                                f'Цена закрытия: {close_cost / 100} \n'
                                f'Обьем торгов: {value_trade / 100} \n'
                                f'Количество сделок: {number_of_trades} \n'
                                f'Минимальная стоимость за торги: {low_cost / 100} \n'
                                f'Максимальная стоимость за торги: {high_cost / 100} </b>\n'
                                , parse_mode='HTML')
                if photo is not None:
                    with open(photo, 'rb') as graph_photo:
                        bot.sendPhoto(chat_id, graph_photo)
                        os.remove(photo)
            except Unauthorized:
                print(chat_id, 'Forbidden: bot was blocked by the user')
                remove_cron(chat_id=chat_id, emitet=emitet.upper(), cron_type='notification')


def get_working_days():
    working_days_list = []
    calendar = db_session.query(Calendar.date).all()
    for day in calendar:
        working_days_list.append(day[0])
    return working_days_list


def main():
    working_days_list = get_working_days()
    while True:
        if str(datetime.now().date()) in working_days_list:
            print('today is working day')
            schedule.every().day.at("09:00").do(job)
            schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    main()

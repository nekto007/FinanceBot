import os
import time
from datetime import datetime

import schedule
import telegram

from api.moex.price import get_price
from configs import settings
from db.db_connect import db_session
from db_models import (
    Calendar,
    Cron,
)

working_days_list = []
calendar = db_session.query(Calendar.date).all()
for day in calendar:
    working_days_list.append(day[0])


def job():
    bot = telegram.Bot(settings.BOT_API_KEY)
    subscribes_list = db_session.query(Cron.sec_id, Cron.chat_id) \
        .filter(Cron.cron_status == 1, Cron.cron_type == 'notification').all()
    if subscribes_list:
        f'<b>Текущая дата: {datetime.now().date()}\n'
        for subscribe in subscribes_list:
            price = get_price(subscribe[0].upper())
            if price["close_price"]:
                close_price = f'Цена закрытия: {price["close_price"]} \n'
            else:
                close_price = f''
            bot.sendMessage(subscribe[1],
                            f'<b>Наименование компании: {price["company_name"]}\n'
                            f'Наименование тикета: {price["ticket_name"]} \n'
                            f'Стоимость акции: {(price["current_cost"])} \n'
                            f'Цена открытия: {price["open_price"]} \n'
                            f'{close_price}'
                            f'Минимальная стоимость за торги: {price["low_cost_daily"]} \n'
                            f'Максимальная стоимость за торги: {price["high_cost_daily"]} </b>\n'
                            , parse_mode='HTML')
            if price['graph_photo'] is not None:
                with open(price['graph_photo'], 'rb') as graph_photo:
                    bot.sendPhoto(subscribe[1], graph_photo)
                    os.remove(price['graph_photo'])


def main():
    while True:
        if str(datetime.now().date()) in working_days_list:
            schedule.run_pending()
            schedule.every().day.at("09:00").do(job)
        time.sleep(10)


if __name__ == '__main__':
    main()

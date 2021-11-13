import logging
import os
import time
from api.moex.currency import get_currency_api
from datetime import (
    datetime,
)

import schedule
import telegram
from telegram.error import Unauthorized

from api.moex.price import (
    get_previous_working_day,
    get_stock_history_previous_day,
    get_trand,
    get_working_days,
)
from configs import settings
from cron.crons import remove_cron
from db.db_connect import db_session
from db_models import (
    Cron,
)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def job():
    bot = telegram.Bot(settings.BOT_API_KEY)
    subscribes_list = db_session.query(Cron.sec_id, Cron.chat_id) \
        .filter(Cron.cron_status == 1, Cron.cron_type == 'notification').all()
    if subscribes_list:
        for subscribe in subscribes_list:
            emitet, chat_id = subscribe
            trand = get_trand(emitet)
            history_info = get_stock_history_previous_day(emitet)
            if history_info is not None:
                short_name, sec_id, open_cost, close_cost, value_trade, numb_of_trade, low_cost, high_cost, trade_date \
                    = history_info[0]
                photo = history_info[1]
                if trand[1] == 1:
                    trand_course = 'Тренд положительный'
                else:
                    trand_course = 'Тренд отрицательный'
                try:
                    bot.sendMessage(chat_id, f'<b>Текущая дата: {datetime.now().date()}\n'
                                             f'Здравствуйте!\n Вы получили это сообщение, т.к. '
                                             f'подписались на автоматическую рассылку обновлений!</b>',
                                    parse_mode='HTML')
                    bot.sendMessage(chat_id,
                                    f'<b>Наименование компании: {short_name}\n'
                                    f'Наименование тикета: {sec_id} \n'
                                    f'Цена открытия: {open_cost / 100} \n'
                                    f'Цена закрытия: {close_cost / 100} \n'
                                    f'Обьем торгов: {value_trade / 100} \n'
                                    f'Количество сделок: {numb_of_trade} \n'
                                    f'Значение скользящей за 15 дней: {trand[3]} \n'
                                    f'Значение скользящей за 50 дней: {trand[4]} \n'
                                    f'Тренд стоимости акции: {trand_course} \n'
                                    f'Текущий тренд держится дней: {trand[2]} \n'
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
            else:
                bot.sendMessage(chat_id, f'<b>По выбранному тикеру: {emitet} на данный момент не было сделок.</b>',
                                parse_mode='HTML')


def main():
    working_days_list = get_working_days()
    schedule.every().day.at("09:00:00").do(job)
    schedule.every().day.at("09:05:00").do(get_currency_api)
    while True:
        if str(datetime.now()) in working_days_list:
            print('today is working day')
            schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    main()

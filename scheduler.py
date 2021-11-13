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
    get_graph,
    get_previous_working_day,
    get_price,
    get_stock_history,
    get_trand,
    get_working_days,
)
from configs import settings
from cron.crons import remove_cron
from db.db_connect import db_session
from db_models import (
    Cron,
    StockHistory,
)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def send_notifications():
    bot = telegram.Bot(settings.BOT_API_KEY)
    subscribes_list = db_session.query(Cron.sec_id, Cron.chat_id) \
        .filter(Cron.cron_status == 1, Cron.cron_type == 'notification').all()
    if subscribes_list:
        for subscribe in subscribes_list:
            emitet, chat_id = subscribe
            trand = get_trand(emitet)
            previous_working_day = get_previous_working_day()
            history_data = get_stock_history(emitet, previous_working_day)
            if history_data:
                history_info = db_session.query(
                    StockHistory.short_name,
                    StockHistory.sec_id,
                    StockHistory.open_cost,
                    StockHistory.close_cost,
                    StockHistory.value_trade,
                    StockHistory.number_of_trades,
                    StockHistory.low_cost,
                    StockHistory.high_cost,
                    StockHistory.trade_date).filter(StockHistory.sec_id == emitet,
                                                    StockHistory.trade_date == str(
                                                        previous_working_day)).first()
                short_name, sec_id, open_cost, close_cost, value_trade, numb_of_trade, low_cost, high_cost, trade_date \
                    = history_info
                photo = get_graph(emitet, 15)
                if trand[1] == 1:
                    trand_course = 'Вверх'
                else:
                    trand_course = 'Вниз'
                try:
                    bot.sendMessage(chat_id, f'<b>Текущая дата: {datetime.now().date()}\n'
                                             f'Здравствуйте!\n Вы получили это сообщение, т.к. '
                                             f'подписались на автоматическую рассылку обновлений!</b>',
                                    parse_mode='HTML')
                    bot.sendMessage(chat_id,
                                    f'<b>Наименование компании: {short_name}\n'
                                    f'Наименование тикета: {sec_id} \n'
                                    f'Цена открытия: {"{:,.2f}₽".format(open_cost / 100)} \n'
                                    f'Цена закрытия: {"{:,.2f}₽".format(close_cost / 100)} \n'
                                    f'Обьем торгов: {"{:,.2f}₽".format(value_trade / 100)} \n'
                                    f'Количество сделок: {"{:,}".format(numb_of_trade)} \n'
                                    f'Скользящая за 15 дней: {"{:,.2f}₽".format(trand[3])} \n'
                                    f'Скользящая за 50 дней: {"{:,.2f}₽".format(trand[4])} \n'
                                    f'Тренд стоимости акции: {trand_course} \n'
                                    f'Текущий тренд держится дней: {trand[2]} \n'
                                    f'Min стоимость за торги: {"{:,.2f}₽".format(low_cost / 100)} \n'
                                    f'Max стоимость за торги: {"{:,.2f}₽".format(high_cost / 100)} </b>\n'
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


def send_alerts():
    bot = telegram.Bot(settings.BOT_API_KEY)
    alerts_list = db_session.query(Cron.sec_id, Cron.chat_id, Cron.sum) \
        .filter(Cron.cron_status == 1, Cron.cron_type == 'alert').all()
    if alerts_list:
        for alert in alerts_list:
            emitet, chat_id, sum = alert
            price = get_price(emitet)
            if price is not None and price != 'Нет сделок' and sum == price[1]:
                photo = get_graph(emitet, 15)
                try:
                    sec_id, current_cost, open_cost, close_cost, low_cost_daily, high_cost_daily, short_name = price
                    if open_cost > sum:
                        trand = 'упала до ожидаемой'
                    else:
                        trand = 'выросла до ожидаемой'
                    bot.sendMessage(chat_id,
                                    f'<b>Текущая дата: {datetime.now().date()}\n'
                                    f'<strong>Цена {short_name}({sec_id}) {trand}: {sum / 100}</strong> \n'
                                    f'Текущая стоимость акции: {(price[1])} \n'
                                    f'Цена открытия: {"{:,.2f}₽".format(open_cost / 100)} \n'
                                    f'Цена закрытия: {"{:,.2f}₽".format(close_cost / 100)} \n'
                                    f'Min стоимость за торги: {"{:,.2f}₽".format(low_cost_daily / 100)} \n'
                                    f'Max стоимость за торги: {"{:,.2f}₽".format(high_cost_daily / 100)} </b>\n'
                                    , parse_mode='HTML')
                    if photo is not None:
                        with open(photo, 'rb') as graph_photo:
                            bot.sendPhoto(chat_id, graph_photo)
                            os.remove(photo)
                except Unauthorized:
                    print(chat_id, 'Forbidden: bot was blocked by the user')
                    remove_cron(chat_id=chat_id, emitet=emitet.upper(), cron_type='alert')


def main():
    working_days_list = get_working_days()
    schedule.every().day.at("09:05:00").do(get_currency_api)
    schedule.every().day.at('09:00:00').do(send_notifications)
    schedule.every().hour.at('00:00').until('20:00').do(send_alerts)
    while True:
        if str(datetime.now()) in working_days_list:
            print('today is working day')
            print(schedule.next_run())
            schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    main()

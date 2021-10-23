from api.moex.price import get_currency_api
import datetime


def get_all_currency(update, context):
    currency_array = get_currency_api()
    print(currency_array['USD/RUB'], currency_array['EUR/RUB'])
    update.message.reply_text(
        f'<b>Текущая дата: {datetime.datetime.now().date()}\n'
        f"Текущая котировка USD/RUB : {currency_array['USD/RUB']}\n"
        f"Текущая котировка EUR/RUB : {currency_array['EUR/RUB']}</b>\n",
        parse_mode='HTML'
    )

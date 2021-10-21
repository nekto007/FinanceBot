from api.moex.price import get_currency_api


def get_currency(update, context):
    currency_answer = update.message.reply_text(get_currency_api())
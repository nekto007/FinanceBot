import logging, settings, requests
import auth, helper, get_stock
from requests.auth import HTTPBasicAuth
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def start(update, context):
    #username = update.message.from_user
    username = update.message.chat.username
    update.message.reply_text(f'Hello {username}! This is MOEX unofficial info bot. Please use /help command to observe available requests.')

def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', helper.help))
    dp.add_handler(CommandHandler('get', get_stock.get_stock))
    auth.auth()
    logging.info("The bot has been started")
    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()
import logging, settings, requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

requests.get(settings.MOEX_AUTH_URL, auth=HTTPBasicAuth(settings.EMAIL, settings.PASSWORD))

def start(update, context):
    print('/started')
    print(update.message)
    update.message.reply_text(f'Hello user! You have launched the start command')

def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', start))
    logging.info("The bot has been started")
    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()
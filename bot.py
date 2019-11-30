# создаем телеграм бота
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot, ReplyKeyboardMarkup, KeyboardButton
from telegram.utils.request import Request

import config
import dump

req = Request(proxy_url=config.proxy)
bot = Bot(config.token, request=req)
upd = Updater(bot=bot, use_context=True)
dp = upd.dispatcher

# логирование
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# приветственное сообщение
def hello(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hello! My name is {0}".format(config.name))

# добавляем приветственное сообщение при команде старт
dp.add_handler(CommandHandler('start', hello))

def main():
    # запускаем бота
    upd.start_polling()
    upd.idle()

if __name__ == '__main__':
    main()

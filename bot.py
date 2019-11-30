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

last_photo = None

# логирование
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# приветственное сообщение
def hello(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Привет, я бот Ева!".format(config.name))
    request_photo(context.bot,chat_id=update.effective_chat.id)


def request_photo(bot,chat_id):
    bot.send_message(chat_id=chat_id,
                     text="Пришли мне пожалуйста, фотографию :)")



def request_location(chat_id):
    location_keyboard = KeyboardButton(text="Send location", request_location=True)
    custom_keyboard = [[ location_keyboard ]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=chat_id,
                     text="Пришли мне пожалуйста, свое местоположение :)",
                     reply_markup=reply_markup)


def location_callback(update, context):
    dump.data_with_location('photo', bot.get_file(last_photo), update.message.from_user.username,
                            update.message.location)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Спасибо! А эта фоточка для вас:")


def photo_callback(update, context):
    global last_photo
    last_photo = update.message.photo[-1].file_id
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Спасибо за фотографию. Она прекрасна.")
    request_location(update.effective_chat.id)


mh = MessageHandler(Filters.location, location_callback)
ph = MessageHandler(Filters.photo, photo_callback)
dp.add_handler(mh)
dp.add_handler(ph)

# добавляем приветственное сообщение при команде старт
dp.add_handler(CommandHandler('start', hello))

def main():
    # запускаем бота
    upd.start_polling()
    upd.idle()

if __name__ == '__main__':
    main()

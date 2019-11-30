# Urban Walk Bot LEGO
В этом репозитории вы найдете составные части вашего бота, из которых вы его сможете
собрать, примерно также как можно собрать что-нибудь из конструктора ЛЕГО.

Файл `bot.py` содержит базовую конфигурация бота, которая просто работает, но ничего
специального не делает. В него вы можете добавлять разные кусочки отсюда.

Не пугайтесь, что здесь многое непонятно -- многие вещи мы более подробно обсудим
в классе. Этот текст нужен для вас скорее как шпаргалка, чтобы вы подсматривали
в него. Не стесняйтесь задавать вопросы, если что-то непонятно! Баларам и Наташа
с радостью вам ответят.

## Обработчики

Вот так выглядит обработчик (handler по-английски) который срабатывает каждый раз,
когда какой-нибудь пользователь присылает фотографию
```
mh = MessageHandler(Filters.photo, photo_callback)
```
Каждый раз когда он срабатывает, вызывается функция `photo_callback`, а что именно
она делает вы указываете сами.

Вот примеры обработчиков сообщений других типов:
```
MessageHandler(Filters.location, location)
MessageHandler(Filters.voice, voice)
```

В некоторых случаях может понадобится более сложный `ConversationHandler`. Вот
пример его использования:
```
ConversationHandler(
    entry_points=[CommandHandler('start', start)],

    states={
        GENDER: [MessageHandler(Filters.regex('^(Boy|Girl|Other)$'), gender)],

        PHOTO: [MessageHandler(Filters.photo, photo),
                CommandHandler('skip', skip_photo)],

        LOCATION: [MessageHandler(Filters.location, location),
                   CommandHandler('skip', skip_location)],

        BIO: [MessageHandler(Filters.text, bio)]
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)
```

Важно не забывать добавлять обработчики в бот, чтобы он про них знал!
```
dp.add_handler(mh)
```

## Запрос локации

Вот этот кусочек кода поможет вам запросить локацию у пользователя:

```
location_keyboard = KeyboardButton(text="Send location", request_location=True)
custom_keyboard = [[ location_keyboard ]]
reply_markup = ReplyKeyboardMarkup(custom_keyboard)
bot.send_message(chat_id=chat_id,
                 text="Пришли мне пожалуйста, свое местоположение :)",
                 reply_markup=reply_markup)
```


## Сохранение данных

Для того чтобы сохранять данные, стоит использовать уже готовую функцию `dump.data_with_location`.
Вот пример ее использования:
```
#где-то в фото:
photo_id  = update.message.photo[-1].file_id

#сохраняем данные
dump.data_with_location("photo", bot.get_file(photo_id),
                        update.message.from_user.username,
                        update.message.location)
                        
# для войса:
voice_id = update.message.voice.file_id

# сохраняем
dump.data_with_location("voice", bot.get_file(voice_id),
                        update.message.from_user.username,
                        update.message.location)
```

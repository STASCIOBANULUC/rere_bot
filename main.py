import telebot
import sqlite3

DEBUG = True

TOKEN = '1833468443:AAEKSzZZ-ymQo_6WVYsT38XzxIiOdlwreR0'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет!')

    # БАЗА ДАННЫХ
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_id(
                id INTEGER 
            )''')
    connect.commit()

    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM user_id WHERE id = {people_id}")
    data = cursor.fetchone()
    # Проверяем на уникальность user_id
    if data is None:
        users_id = [message.chat.id]
        cursor.execute("INSERT INTO user_id VALUES(?);", users_id)
        connect.commit()
    elif DEBUG:
        bot.send_message(message.chat.id, 'Такой пользователь уже существует')

    def keyboard_func():
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('Привет', 'Пока')
        bot.send_message(message.chat.id, 'Привет!', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_message(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет!')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Пока!')


string = 'Вот здесь я изменил файл'


@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = r'C:\Users\Admin\PycharmProjects\me_editing_bot\ ' + message.document.file_name

        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Пожалуй, я сохраню это")

        bot.reply_to(message, "Пожалуй, я изменю его")
        with open(src, 'w+') as new_file:
            new_file.write(string)

        re_file = open(src)
        bot.send_document(message.chat.id, re_file)

        bot.reply_to(message, "Я изменил файл, если что-то не так обратитесь в поддержку")

    except Exception as e:
        if DEBUG:
            bot.reply_to(message, e)


bot.polling(none_stop=True)

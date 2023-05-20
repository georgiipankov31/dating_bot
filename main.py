from datetime import *
from telebot import *
import psycopg2
import psycopg2.extras
import logging
from telebot.types import  ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
con = psycopg2.connect(
  database="goshavvpan", 
  user="goshavvpan",
  password="sL7ea9wBcrW5hUb",
  host="pg2.sweb.ru",
  port="5432"
)
cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)  
bot = telebot.TeleBot("6254079896:AAFjlsTdC6uPuWSKhxSaxhnHwptoviWBa_M")
@bot.message_handler(commands=['start'])
def start(massage):
    try:
        print(message.from_user.username)
        cur.execute(f'insert into dating.users (user_id, user_nick, user_city) values ({message.chat.id}, {message.from_user.username}, "empty");')
        con.commit()
    except:
        unknown_error(massage)
def unknown_error(massage):
    try:
        bot.send_message(massage.chat.id, 'Неизвсетная ошибка! Напишите в поддержку!')
    except:
        print('Fatal Error')

while True:
    try:
        bot.polling(non_stop=True)
    except telebot.apihelper.ApiException as e:
        logging.error(e)
        bot.stop_polling()
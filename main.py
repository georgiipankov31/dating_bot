from datetime import *
from telebot import *
import psycopg2
from dadata import Dadata
import psycopg2.extras
import logging
from telebot.types import  ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from geopy.geocoders import Nominatim
con = psycopg2.connect(
  database="goshavvpan", 
  user="goshavvpan",
  password="sL7ea9wBcrW5hUb",
  host="pg2.sweb.ru",
  port="5432"
)
cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)  
bot = telebot.TeleBot("6254079896:AAFjlsTdC6uPuWSKhxSaxhnHwptoviWBa_M")
markup_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_finding = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_can = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1_can = types.KeyboardButton("❌")
markup_can.add(btn1_can)
btn1_main = types.KeyboardButton("🚀")
btn2_main = types.KeyboardButton("⚙️")
markup_main.add(btn1_main, btn2_main)
markup_anketa = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1_anketa = types.KeyboardButton("🚀")
btn2_anketa = types.KeyboardButton("😴") 
markup_anketa.add(btn1_anketa, btn2_anketa)
markup_ug = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1_ug = types.KeyboardButton("🚹")
btn2_ug = types.KeyboardButton("🚺")
markup_ug.add(btn1_ug, btn2_ug)
markup_fg = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1_fg = types.KeyboardButton("🙎‍♂")
btn2_fg = types.KeyboardButton("🙎‍♀")
btn3_fg = types.KeyboardButton("🚻")
keyboard_l = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button_loc = types.KeyboardButton(text="📍Отправить координату", request_location=True)
keyboard_l.add(button_loc)
markup_fg.add(btn1_fg, btn2_fg, btn3_fg)
markup_del = InlineKeyboardMarkup()
markup_type = InlineKeyboardMarkup(row_width=1)
markup_type.add(InlineKeyboardButton(text='💘👥 Дружба и отношения', callback_data='friend_rel'))
markup_type.add(InlineKeyboardButton(text='👥 Дружба', callback_data='friend'))
markup_type.add(InlineKeyboardButton(text='💘 Отношения', callback_data='rel'))
markup_type.add(InlineKeyboardButton(text='💼 Деловое и все остальное', callback_data='diff'))
markup_type.add(InlineKeyboardButton(text='◀️ Вернуться назад', callback_data='back_second'))
markup_option = InlineKeyboardMarkup(row_width=1)
markup_option.add(InlineKeyboardButton(text='🚻 Пол в анкетах', callback_data='f_gender'))
markup_option.add(InlineKeyboardButton(text='🫴 Возраст в анкетах', callback_data='f_age'))
markup_option.add(InlineKeyboardButton(text='ℹ️ Тип анкет', callback_data='f_type'))
markup_option.add(InlineKeyboardButton(text='◀️ Вернуться назад', callback_data='back'))
markup_anketa2 = InlineKeyboardMarkup(row_width=1)
markup_anketa2.add(InlineKeyboardButton(text='📷 Изменить фото', callback_data='photo'))
markup_anketa2.add(InlineKeyboardButton(text='📩 Изменить текст анкеты', callback_data='text'))
markup_anketa2.add(InlineKeyboardButton(text='💡 Изменить имя', callback_data='name'))
markup_anketa2.add(InlineKeyboardButton(text='📍 Изменить возраст', callback_data='age'))
markup_anketa2.add(InlineKeyboardButton(text='🌆 Изменить город', callback_data='city'))
markup_anketa2.add(InlineKeyboardButton(text='🚻 Изменить мой пол', callback_data='my_gender'))
markup_anketa2.add(InlineKeyboardButton(text='🔍 Изменить критерии поиска', callback_data='option'))
def unknown_error(message):
    try:
        bot.send_message(message.chat.id, 'Неизвсетная ошибка! Напишите в поддержку!')
    except:
        print('Fatal Error')
@bot.message_handler(commands=['start'])
def start(message):
    try:
        global markup_main
        cur.execute(f"select * from dating.users where user_id = {message.chat.id}")
        data = cur.fetchall()
        if len(data) == 0:
            if message.from_user.username == None:
                bot.send_message(message.chat.id, 'У вас нет короткого имени.\n\nЭто обязательное условия для использования нашего бота.\n\nИнструкция ниже: \nhttps://www.youtube.com/watch?v=muxNQ4HmTyE')
                bot.register_next_step_handler(message, start)
            else: 
                full_name = message.from_user.first_name
                cur.execute(f"insert into dating.users (user_id, user_nick, user_name, user_city) values ({message.chat.id}, '{message.from_user.username}', '{full_name}','empty');")
                con.commit()
                bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}. Для пользования нашим ботом необходимо ввести город. Напиши название своего города на русском.', reply_markup=types.ReplyKeyboardRemove())
                bot.register_next_step_handler(message, set_city)
        else:
            bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}.' , reply_markup=markup_main)
    except:
        unknown_error(message)
def set_city(message):
    try:
        if message.text == '/location':
            global keyboard_l
            bot.send_message(message.chat.id, 'Отправь локацию.', reply_markup=keyboard_l)
            bot.register_next_step_handler(message, location)
        elif message.text == '/region':
            bot.send_message(message.chat.id, 'Отправьте номер вашего региона и мы покажем вам, какие города есть.')
            bot.register_next_step_handler(message, region)
        else:
            cur.execute('select city_name from dating.city;')
            cit = cur.fetchall()
            is_find = False
            for i in cit:
                if i[0] == message.text.lower().replace('-', '').replace(' ', ''):
                    cur.execute(f"update dating.users set user_city = '{i[0]}' where user_id = {message.chat.id}")
                    con.commit()
                    is_find = True
                    break
            if is_find == False:
                bot.send_message(message.chat.id, 'Похоже, что такого города нету в нашей базе.\n\nПопробуй ввести свой регион(число) /region\n\nИли отправь мне свою локацию /location\n\nИли еще раз отправь название города.')
                bot.register_next_step_handler(message, set_city)
            else:
                city_text = message.text.lower()
                bot.send_message(message.chat.id, f"Отлично! Буду показывать анкеты из города {city_text.title()}\n\nТеперь введи свой возраст:")
                bot.register_next_step_handler(message, set_age)
    except:
        unknown_error(message)
def region(message):
    try:
        if message.text.isnumeric():
            cur.execute(f'select * from dating.city where city_region = {message.text}')
            data = cur.fetchall()
            if len(data) == 0:
                bot.send_message(message.chat.id, f"Нет такого региона, введите ваш регион еще раз:")
                bot.register_next_step_handler(message, region)
            else:
                string = ''
                for i in range(len(data)):
                    string = string + '📍 ' + data[i][0].title() + '\n'
                bot.send_message(message.chat.id, f"Вот все города которые есть в {data[0][2].title()}:\n\n{string[:-1]}")
                bot.send_message(message.chat.id, f"Теперь введите город:")
                bot.register_next_step_handler(message, set_city)
        else:
            bot.send_message(message.chat.id, f"Это не число, введите ваш регион еще раз:")
            bot.register_next_step_handler(message, region)
    except:
        unknown_error(message)
def set_age(message):
    try:
        if message.text.isnumeric():
            cur.execute(f"update dating.users set user_age = {message.text} where user_id = {message.chat.id}")
            con.commit()
            cur.execute(f"update dating.users set finding_age_min = {int(message.text) - 1}, finding_age_max = {int(message.text) + 1} where user_id = {message.chat.id}")
            con.commit()
            global markup_ug
            bot.send_message(message.chat.id, f"Отлично!\n\nТеперь введи свой пол:", reply_markup=markup_ug)
            bot.register_next_step_handler(message, set_gender)
        else:
            bot.send_message(message.chat.id, f"Это не число, введите ваш возраст еще раз:")
            bot.register_next_step_handler(message, set_age)
    except:
        unknown_error(message)
def set_gender(message):
    try:
        global markup_fg
        if message.text == "🚹":
            cur.execute(f"update dating.users set user_gender = 'male' where user_id = {message.chat.id}")
            con.commit()
            bot.send_message(message.chat.id, f"Мужской пол выставлен. Теперь укажите кого вы ищите.", reply_markup=markup_fg)
            bot.register_next_step_handler(message, setf_gender)
        elif message.text == "🚺":
            cur.execute(f"update dating.users set user_gender = 'female' where user_id = {message.chat.id}")
            con.commit()
            bot.send_message(message.chat.id, f"Женский пол выставлен. Теперь укажите кого вы ищите.", reply_markup=markup_fg)
            bot.register_next_step_handler(message, setf_gender)
        else:
            bot.send_message(message.chat.id, f"Некорректный текст, нажмите на какую-то кнопку.")
            bot.register_next_step_handler(message, set_gender)
    except:
        unknown_error(message)
def update_gender(message):
    try:
        global markup_fg
        global markup_main
        if message.text == "❌":
            bot.send_message(message.chat.id, 'Отменено', reply_markup=markup_main)
        elif message.text == "🚹":
            cur.execute(f"update dating.users set user_gender = 'male' where user_id = {message.chat.id}")
            con.commit()
            bot.send_message(message.chat.id, f"Мужской пол выставлен.", reply_markup=markup_main)
            show_anketa(message)
        elif message.text == "🚺":
            cur.execute(f"update dating.users set user_gender = 'female' where user_id = {message.chat.id}")
            con.commit()
            bot.send_message(message.chat.id, f"Женский пол выставлен.", reply_markup=markup_main)
            show_anketa(message)
        else:
            bot.send_message(message.chat.id, f"Некорректный текст, нажмите на какую-то кнопку.")
            bot.register_next_step_handler(message, set_gender)
    except:
        unknown_error(message)
def set_gender(message):
    try:
        global markup_fg
        if message.text == "🚹":
            cur.execute(f"update dating.users set user_gender = 'male' where user_id = {message.chat.id}")
            con.commit()
            bot.send_message(message.chat.id, f"Мужской пол выставлен. Теперь укажите кого вы ищите.", reply_markup=markup_fg)
            bot.register_next_step_handler(message, setf_gender)
        elif message.text == "🚺":
            cur.execute(f"update dating.users set user_gender = 'female' where user_id = {message.chat.id}")
            con.commit()
            bot.send_message(message.chat.id, f"Женский пол выставлен. Теперь укажите кого вы ищите.", reply_markup=markup_fg)
            bot.register_next_step_handler(message, setf_gender)
        else:
            bot.send_message(message.chat.id, f"Некорректный текст, нажмите на какую-то кнопку.")
            bot.register_next_step_handler(message, set_gender)
    except:
        unknown_error(message)
def setf_gender(message):
    try:
        global markup_anketa
        if message.text == "🙎‍♂":
            cur.execute(f"update dating.users set user_finding_gender = 'male' where user_id = {message.chat.id}")
            con.commit()
            bot.send_message(message.chat.id, f"Мужской пол собеседника выставлен. Вот твоя анкета:", reply_markup=markup_anketa)
            show_anketa(message)
        elif message.text == "🙎‍♀":
            cur.execute(f"update dating.users set user_finding_gender = 'female' where user_id = {message.chat.id}")
            con.commit()
            bot.send_message(message.chat.id, f"Женский пол собеседника выставлен. Вот твоя анкета:", reply_markup=markup_anketa)
            show_anketa(message)
        elif message.text == "🚻":
            cur.execute(f"update dating.users set user_finding_gender = 'trans' where user_id = {message.chat.id}")
            con.commit()
            bot.send_message(message.chat.id, f"Буду показывать тебе всех пользовтелей. Вот твоя анкета:", reply_markup=markup_anketa)
            show_anketa(message)
        else:
            bot.send_message(message.chat.id, f"Некорректный текст, нажмите на какую-то кнопку.")
            bot.register_next_step_handler(message, setf_gender)
    except:
        unknown_error(message)
def location(message):
    try:
        if message.location is not None:
            geolocator = Nominatim(user_agent="Tester")
            location_m = geolocator.reverse(f", {message.location.latitude}, {message.location.longitude}")
            if 'city' in location_m.raw['address']:
                cur.execute(f"select * from dating.city where city_name = '{location_m.raw['address']['city'].lower().replace('-', '').replace(' ', '')}'")
                data = cur.fetchall()
                if len(data) != 0:
                        cur.execute(f"update dating.users set user_city = '{location_m.raw['address']['city'].lower().replace('-', '').replace(' ', '')}' where user_id = {message.chat.id}")
                        con.commit()
                        bot.send_message(message.chat.id, f"Установлен город {location_m.raw['address']['city'].title()} Введите ваш возраст:", reply_markup=types.ReplyKeyboardRemove())
                        bot.register_next_step_handler(message, set_age)
                else:
                    bot.send_message(message.chat.id, f"Нет такого города. введите ваш город текстом еще раз:", reply_markup=types.ReplyKeyboardRemove())
                    bot.register_next_step_handler(message, set_city)
            elif 'state' in location_m.raw['address']:
                cur.execute(f"select * from dating.city where city_data = '{location_m.raw['address']['state'].lower()}'")
                data = cur.fetchall()
                if len(data) != 0:
                    string = ''
                    for i in range(len(data)):
                        string = string + '📍 ' + data[i][0].title() + '\n'
                    bot.send_message(message.chat.id, f"Вот все города которые рядом с вами:\n\n{string[:-1]}")
                    bot.send_message(message.chat.id, f"Теперь введите город:", reply_markup=types.ReplyKeyboardRemove())
                    bot.register_next_step_handler(message, set_city)
                else:
                    bot.send_message(message.chat.id, f"Нет такого города. введите ваш город текстом еще раз:")
                    bot.register_next_step_handler(message, set_city)
            else:
                bot.send_message(message.chat.id, f"Нет такого города. введите ваш город текстом еще раз:")
                bot.register_next_step_handler(message, set_city)    
        else:
            bot.send_message(message.chat.id, 'Вы не отправили локацию. Давайте еще раз.', reply_markup=keyboard_l)
            bot.register_next_step_handler(message, location)
    except:
        unknown_error(message)
def update_location(message):
    try:
        global markup_main
        if message.location is not None:
            geolocator = Nominatim(user_agent="Tester")
            location_m = geolocator.reverse(f", {message.location.latitude}, {message.location.longitude}")
            if 'city' in location_m.raw['address']:
                cur.execute(f"select * from dating.city where city_name = '{location.raw['address']['city'].lower().replace('-', '').replace(' ', '')}'")
                data = cur.fetchall()
                if len(data) != 0:
                        cur.execute(f"update dating.users set user_city = '{location.raw['address']['city'].lower().replace('-', '').replace(' ', '')}'where user_id = {message.chat.id}")
                        con.commit()
                        bot.send_message(message.chat.id, f"Установлен город {location.raw['address']['city'].title()}", reply_markup=markup_main)
                else:
                    bot.send_message(message.chat.id, f"Нет такого города. введите ваш город текстом еще раз:", reply_markup=types.ReplyKeyboardRemove())
                    bot.register_next_step_handler(message, update_city)
            elif 'state' in location_m.raw['address']:
                cur.execute(f"select * from dating.city where city_data = '{location.raw['address']['state'].lower()}'")
                data = cur.fetchall()
                if len(data) != 0:
                    string = ''
                    for i in range(len(data)):
                        string = string + '📍 ' + data[i][0].title() + '\n'
                    bot.send_message(message.chat.id, f"Вот все города которые рядом с вами:\n\n{string[:-1]}")
                    bot.send_message(message.chat.id, f"Теперь введите город:", reply_markup=types.ReplyKeyboardRemove())
                    bot.register_next_step_handler(message, update_city)
                else:
                    bot.send_message(message.chat.id, f"Нет такого города. введите ваш город текстом еще раз:")
                    bot.register_next_step_handler(message, update_city)
            else:
                bot.send_message(message.chat.id, f"Нет такого города. введите ваш город текстом еще раз:")
                bot.register_next_step_handler(message, update_city)    
        else:
            bot.send_message(message.chat.id, 'Вы не отправили локацию. Давайте еще раз.', reply_markup=keyboard_l)
            bot.register_next_step_handler(message, update_location)
    except:
        unknown_error(message)
def update_city(message):
    try:
        global markup_main
        if message.text =='❌':
            bot.send_message(message.chat.id, 'Отменено', reply_markup=markup_main)
        elif message.text == '/location':
            global keyboard_l
            bot.send_message(message.chat.id, 'Отправь локацию.', reply_markup=keyboard_l)
            bot.register_next_step_handler(message, update_location)
        elif message.text == '/region':
            bot.send_message(message.chat.id, 'Отправьте номер вашего региона и мы покажем вам, какие города есть.')
            bot.register_next_step_handler(message, update_region)
        else:
            cur.execute('select city_name from dating.city;')
            cit = cur.fetchall()
            is_find = False
            for i in cit:
                if i[0] == message.text.lower().replace('-', '').replace(' ', ''):
                    cur.execute(f"update dating.users set user_city = '{i[0]}' where user_id = {message.chat.id}")
                    con.commit()
                    is_find = True
                    break
            if is_find == False:
                bot.send_message(message.chat.id, 'Похоже, что такого города нету в нашей базе.\n\nПопробуй ввести свой регион(число) /region\n\nИли отправь мне свою локацию /location\n\nИли еще раз отправь название города.')
                bot.register_next_step_handler(message, update_city)
            else:
                city_text = message.text.lower()
                bot.send_message(message.chat.id, f"Отлично! Буду показывать анкеты из города {city_text.title()}", reply_markup=markup_main)
                show_anketa(message)
    except:
        unknown_error(message)
def update_region(message):
    try:
        if message.text.isnumeric():
            cur.execute(f'select * from dating.city where city_region = {message.text}')
            data = cur.fetchall()
            if len(data) == 0:
                bot.send_message(message.chat.id, f"Нет такого региона, введите ваш регион еще раз:")
                bot.register_next_step_handler(message, update_region)
            else:
                string = ''
                for i in range(len(data)):
                    string = string + '📍 ' + data[i][0].title() + '\n'
                bot.send_message(message.chat.id, f"Вот все города которые есть в {data[0][2].title()}:\n\n{string[:-1]}")
                bot.send_message(message.chat.id, f"Теперь введите город:")
                bot.register_next_step_handler(message, update_city)
        else:
            bot.send_message(message.chat.id, f"Это не число, введите ваш регион еще раз:")
            bot.register_next_step_handler(message, update_region)
    except:
        unknown_error(message)
def show_anketa(message):
    try:
        global markup_anketa2
        cur.execute(f"select user_name, user_gender, user_finding_gender, user_age, user_text, user_city, user_rating, user_photo from dating.users where user_id = {message.chat.id}")
        data = cur.fetchall()
        data = data[0]
        if data[1] == 'male':
            gender_me = 'мужской'
        elif data[1] == 'female':
            gender_me = 'женский'
        else:
            gender_me = 'неопределен'
        if data[2] == 'male':
            gender_f = 'мужчину'
        elif data[2] == 'female':
            gender_f = 'девушку'
        else:
            gender_f = 'всех'
        if data[7] != None:
            bot.send_photo(message.chat.id, data[7])
        bot.send_message(message.chat.id, f"📌 {data[0]}, {data[3]}\n\n🌎 {data[5].title()}\n\n💾 {data[4]}\n\nРейтинг: {data[6]}\n🚹🚺 Пол: {gender_me}\n🚻 Ищу: {gender_f}", reply_markup=markup_anketa2)
    except:
        unknown_error(message)
def update_age(message):
    try:
        global markup_main
        if message.text == "❌":
            bot.send_message(message.chat.id, 'Отменено', reply_markup=markup_main)
        elif message.text.isnumeric():
            cur.execute(f"update dating.users set user_age = {message.text} where user_id = {message.chat.id}")
            con.commit()
            cur.execute(f"update dating.users set finding_age_min = {int(message.text) - 1}, finding_age_max = {int(message.text) + 1} where user_id = {message.chat.id}")
            con.commit()
            bot.send_message(message.chat.id, f"Возраст выставлен. По умолчанию вам будут попадться люди от {int(message.text) - 1} до {int(message.text) + 1} лет, но это можно изменить в настройках.", reply_markup=markup_main)
            show_anketa(message)
        else:
            bot.send_message(message.chat.id, f"Это не число, введите ваш возраст еще раз:")
            bot.register_next_step_handler(message, update_age)
    except:
        unknown_error(message)
def update_name(message):
    try:
        global markup_del
        global markup_main
        if message.text == "❌":
            bot.send_message(message.chat.id, 'Отменено', reply_markup=markup_main)
        elif len(message.text) >= 3 and len(message.text) <= 18:
            cur.execute(f"update dating.users set user_name = '{message.text}' where user_id = {message.chat.id}")
            con.commit()
            bot.send_message(message.chat.id, f'Хорошо, теперь ты - {message.text}', reply_markup=markup_main)
            show_anketa(message)
        else:
            bot.send_message(message.chat.id, 'Введите имя еще раз, оно должно быть от 3 до 18 символов.', reply_markup=markup_del)
            bot.register_next_step_handler(message, update_name)
    except:
        unknown_error(message)
def update_text(message):
    try:
        global markup_del
        global markup_main
        if message.text == "❌":
            bot.send_message(message.chat.id, 'Отменено', reply_markup=markup_main)
        elif len(message.text) >= 1 and len(message.text) <= 3000:
            cur.execute(f"update dating.users set user_text = '{message.text}' where user_id = {message.chat.id}")
            con.commit()
            bot.send_message(message.chat.id, f'Хорошо, теперь у тебя новое описание.', reply_markup=markup_main)
            show_anketa(message)
        else:
            bot.send_message(message.chat.id, 'Введите текст еще раз, оно должно быть от 1 до 3000 символов.', reply_markup=markup_del)
            bot.register_next_step_handler(message, update_name)
    except:
        unknown_error(message)
def update_photo(message):
    try:
        global markup_can
        global markup_main
        if message.content_type == 'photo':
            photo = max(message.photo, key=lambda x: x.height)
            file_id = photo.file_id
            cur.execute(f"update dating.users set user_photo = '{file_id}' where user_id = {message.chat.id}")
            con.commit()
            bot.send_message(message.chat.id, 'Успешно', reply_markup=markup_main)
            show_anketa(message)
        elif(message.content_type == 'text'):
            if message.text == "❌":
                bot.send_message(message.chat.id, 'Отменено', reply_markup=markup_main)
            else:
                bot.send_message(message.chat.id, 'Неподдерживаемый тип. Отправьте фото еще раз.', reply_markup=markup_can)
                bot.register_next_step_handler(message, update_photo)
        else:
            bot.send_message(message.chat.id, 'Неподдерживаемый тип. Отправьте фото еще раз.', reply_markup=markup_can)
            bot.register_next_step_handler(message, update_photo)
    except:
        unknown_error(message)
def update_fage(message):
    try:
        global markup_can
        global markup_main
        if message.text == "❌":
            bot.send_message(message.chat.id, 'Отменено', reply_markup=markup_main)
        else:
            ages = message.text.split()
            if (len(ages) == 2) and (ages[0].isnumeric()) and (ages[1].isnumeric()) and (int(ages[1]) >= int(ages[0])):
                cur.execute(f"update dating.users set finding_age_min = {ages[0]}, finding_age_max = {ages[1]} where user_id = {message.chat.id}")
                con.commit()
                bot.send_message(message.chat.id, f'Успешно! Теперь вам будут попадаться только люди в возрасте от {ages[0]} до {ages[1]}', reply_markup=markup_main)
            else:
                bot.send_message(message.chat.id, 'Некорректные данные. Введите еще раз.\n\nНапример, если вы хотите чтобы вам попадались люди от 15 до 16 лет, то просто напиищшите "15 16"', reply_markup=markup_can)
                bot.register_next_step_handler(message, update_fage)
    except:
        unknown_error(message)
def update_fgender(message):
    try:
        global markup_anketa
        if message.text == "🙎‍♂":
            cur.execute(f"update dating.users set user_finding_gender = 'male' where user_id = {message.chat.id}")
            con.commit()
            bot.send_message(message.chat.id, f"Мужской пол собеседника выставлен. Вот твоя анкета:", reply_markup=markup_anketa)
            show_anketa(message)
        elif message.text == "🙎‍♀":
            cur.execute(f"update dating.users set user_finding_gender = 'female' where user_id = {message.chat.id}")
            con.commit()
            bot.send_message(message.chat.id, f"Женский пол собеседника выставлен. Вот твоя анкета:", reply_markup=markup_anketa)
            show_anketa(message)
        elif message.text == "🚻":
            cur.execute(f"update dating.users set user_finding_gender = 'trans' where user_id = {message.chat.id}")
            con.commit()
            bot.send_message(message.chat.id, f"Буду показывать тебе всех пользовтелей. Вот твоя анкета:", reply_markup=markup_anketa)
            show_anketa(message)
        else:
            bot.send_message(message.chat.id, f"Некорректный текст, нажмите на какую-то кнопку.")
            bot.register_next_step_handler(message, update_fgender)
    except:
        unknown_error(message)
@bot.message_handler(content_types=['text'])
def main_menu(message):
    try:
        global markup_main
        global markup_finding
        if message.text == '⚙️':  
            show_anketa(message)
            bot.send_message(message.chat.id, 'Автор бота: @gpankov31', reply_markup=markup_anketa)
        elif message.text == '🚀':
            cur.execute(f"update dating.users  set is_actually  = true where user_id = {message.chat.id};")
            con.commit()
            bot.send_message(message.from_user.id, '🔎 Поиск...', reply_markup=markup_finding)
        elif message.text == '😴':
            cur.execute(f"update dating.users  set is_actually  = false where user_id = {message.chat.id};")
            con.commit()
            bot.send_message(message.from_user.id, 'Анкета была отключена. Теперь вы не будете попадаться никому.', reply_markup=markup_main)
        elif (message.text == '❌'):
            bot.send_message(message.from_user.id, 'Отменено.', reply_markup=markup_main)
        else:
            angry_list = ["😡Чумба ты совсем конченный? я тебя не понимаю... сходи к доктору, попей таблеточки😡", "🤬ыыЫЫЫыыыэээ ба бу бэ йй я не понимаю🤬", "😯Без понятия о чем ты, человек😯", "🥺Меня не запрограмировали на такие умные команды....🥺", "🧐Ты о чем??🧐", "🤡Что.Ты.Несешь.🤡"]
            bot.send_message(message.from_user.id, text=random.choice(angry_list), reply_markup=markup_main)
    except:
        unknown_error(message)
@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
        try:
            global markup_del
            global markup_can
            global markup_option
            global markup_fg
            global markup_ug
            global markup_type
            if call.message:
                if call.data == 'photo':
                    bot.send_message(call.message.chat.id, 'Отправьте фото:', reply_markup=markup_can)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Следуйте инструкции.', reply_markup=markup_del)
                    bot.register_next_step_handler(call.message, update_photo)
                elif call.data == 'text':
                    bot.send_message(call.message.chat.id, 'Введите текст:', reply_markup=markup_can)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Следуйте инструкции.', reply_markup=markup_del)
                    bot.register_next_step_handler(call.message, update_text)
                elif call.data == 'name':
                    bot.send_message(call.message.chat.id, 'Как мне тебя называть?', reply_markup=markup_can)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Следуйте инструкции.', reply_markup=markup_del)
                    bot.register_next_step_handler(call.message, update_name)
                elif call.data == 'age':
                    bot.send_message(call.message.chat.id, 'Введите возраст:', reply_markup=markup_can)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Следуйте инструкции.', reply_markup=markup_del)
                    bot.register_next_step_handler(call.message, update_age)
                elif call.data == 'city':
                    bot.send_message(call.message.chat.id, 'Введите ваш город:', reply_markup=markup_can)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Следуйте инструкции.', reply_markup=markup_del)
                    bot.register_next_step_handler(call.message, update_city)
                elif call.data == 'my_gender':
                    bot.send_message(call.message.chat.id, 'Введите ваш пол:', reply_markup=markup_ug)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Следуйте инструкции.', reply_markup=markup_del)
                    bot.register_next_step_handler(call.message, update_gender)
                elif call.data == 'option':
                    bot.send_message(call.message.chat.id, 'Выберите опцию', reply_markup=markup_option)
                elif call.data == 'back':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Вы вернулись назад.', reply_markup=markup_del)
                elif call.data == 'f_gender':
                    bot.send_message(call.message.chat.id, 'Введите пол:', reply_markup=markup_fg)
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Следуйте инстуркции.', reply_markup=markup_del)
                    bot.register_next_step_handler(call.message, update_fgender)
                elif call.data == 'f_age':
                    cur.execute(f'select finding_age_min, finding_age_max from dating.users where user_id = {call.message.chat.id}')
                    data = cur.fetchall()
                    data = data[0]
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Следуйте инстуркции.', reply_markup=markup_del)
                    bot.send_message(call.message.chat.id, f'Минимальный возраст: {data[0]}\nМаксимальный возраст: {data[1]}\n\nВведите 2 числа через пробел, где первое будет являться минимальным новым возрастом, а второе максимальным.', reply_markup=markup_can)
                    bot.register_next_step_handler(call.message, update_fage)
                elif call.data == 'f_type':
                    cur.execute(f"select user_type from dating.users where user_id = {call.message.chat.id}")
                    textl = cur.fetchall()
                    if textl[0][0] == 'fr':
                        textl = 'друзей и отношения.'
                    elif textl[0][0] == 'r':
                        textl = 'отношения.'
                    elif textl[0][0] == 'f':
                        textl = 'дружбу.'
                    else:
                        textl = 'деловые отношения и остальное.'
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Следуйте инстуркции. Сейчас вы ищите {textl}', reply_markup=markup_del)
                    bot.send_message(call.message.chat.id, f'Выберите тип вашей анкеты', reply_markup=markup_type)
                elif call.data == 'friend_rel':
                    cur.execute(f"update dating.users set user_type = 'fr' where user_id = {call.message.chat.id}")
                    con.commit()
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Ты ищешь друзей или отношения', reply_markup=markup_del)
                elif call.data == 'friend':
                    cur.execute(f"update dating.users set user_type = 'f' where user_id = {call.message.chat.id}")
                    con.commit()
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Ты ищешь друзей.', reply_markup=markup_del)
                elif call.data == 'rel':
                    cur.execute(f"update dating.users set user_type = 'r' where user_id = {call.message.chat.id}")
                    con.commit()
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Ты ищешь отношения', reply_markup=markup_del)
                elif call.data == 'diff':
                    cur.execute(f"update dating.users set user_type = 'd' where user_id = {call.message.chat.id}")
                    con.commit()
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Ты ищешь деловые предложения или что-то другое.', reply_markup=markup_del)
                elif call.data == 'back_second':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Вы вернулись назад.', reply_markup=markup_option)
        except:
            print('error callback')
while True:
    try:
        bot.polling(non_stop=True)
    except telebot.apihelper.ApiException as e:
        logging.error(e)
        bot.stop_polling()

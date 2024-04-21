import telebot
from telebot import types
from config import BOT_TOKEN
from data.get_message import *
from data.db.query import *
from data.db.work_with_table import *

token = BOT_TOKEN
bot = telebot.TeleBot(token)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    call_funk = callback.data
    message = callback.message
    if call_funk == 'insert_data':
        get_data_from_user(message)
    elif call_funk[:6] == 'change':
        get_parameter(message, call_funk[7:])
    elif call_funk == 'watch_inf':
        watch_inf(message)


@bot.message_handler(commands=['start'])
def start_message(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("/help"))
    markup.add(types.KeyboardButton("/start"))

    bot.send_message(message.chat.id, get_message(0), reply_markup=markup)

    if is_unique_user(message.chat.id):
        insert_id(message.chat.id)
    start2_message(message)


def start2_message(message):
    markup1 = types.InlineKeyboardMarkup()
    markup1.add(types.InlineKeyboardButton('Ввести данные', callback_data='insert_data'))
    bot.send_message(message.chat.id, get_message(1), reply_markup=markup1)


@bot.message_handler(commands=['help'])
def help_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/watch_inf")
    btn2 = types.KeyboardButton("/stop_session")
    btn3 = types.KeyboardButton("/change_data")
    btn4 = types.KeyboardButton("/show_data")
    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(message.chat.id, get_message(2))


def get_data_from_user(message):
    bot.send_message(message.chat.id, get_message(3))
    bot.register_next_step_handler(message, insert_from_user)


def insert_from_user(message):
    try:
        if is_unique_user(message.chat.id):
            insert_id(message.chat.id)
        credit_, interest_rate_, months_, = message.text.split(", ")
        push_inf(credit_, interest_rate_, months_, message.chat.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(get_message(4), callback_data='watch_inf'))
        bot.send_message(message.chat.id, get_message(5), reply_markup=markup)
    except Exception:
        bot.send_message(message.chat.id, get_message(16))
        start2_message(message)


@bot.message_handler(commands=['watch_inf'])
def watch_inf(message):
    try:
        create_table(message.chat.id)
        bot.send_photo(message.chat.id, open(f'{PATH_FOR_TABLES}table{message.chat.id}.png', 'rb'))
    except Exception:
        bot.send_message(message.chat.id, get_message(13))


@bot.message_handler(commands=['stop_session'])
def stop_session(message):
    try:
        delete_table_inf(message.chat.id)

        try:
            delete_img(message.chat.id)
            bot.send_message(message.chat.id, get_message(6))
        except Exception:
            bot.send_message(message.chat.id, get_message(6))
    except Exception:
        bot.send_message(message.chat.id, get_message(14))


@bot.message_handler(commands=['change_data'])
def get_type_change_data(message):
    markup1 = types.InlineKeyboardMarkup()
    markup1.add(types.InlineKeyboardButton(get_message(7), callback_data='change_Pv'))
    markup1.add(types.InlineKeyboardButton(get_message(8), callback_data='change_Ry'))
    markup1.add(types.InlineKeyboardButton(get_message(9), callback_data='change_Ly'))

    bot.send_message(message.chat.id, get_message(10), reply_markup=markup1)


def get_parameter(message, prmtr):
    bot.send_message(message.chat.id, get_message(11))
    bot.register_next_step_handler(message, change_data, prmtr)


def change_data(message, prmtr):
    if get_data(message.chat.id) is None:
        bot.send_message(message.chat.id, get_message(15))
        start2_message(message)
    else:
        change_prmtr(message.chat.id, prmtr, message.text)
        bot.send_message(message.chat.id, get_message(12))


@bot.message_handler(commands=['show_data'])
def show_data(message):
    try:
        results = get_data(message.chat.id)
        if results is None:
            bot.send_message(message.chat.id, get_message(13))
            start2_message(message)
        else:
            reply = f"{get_message(7)} {results[0]}\n{get_message(8)} = {results[1]}\n{get_message(9)} = {results[2]}"
            bot.send_message(message.chat.id, reply)
    except Exception:
        bot.send_message(message.chat.id, get_message(13))
        start2_message(message)



bot.infinity_polling()

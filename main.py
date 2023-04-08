import telebot
from telebot import types
from models.signs import Sign
from scraper.scraper import *

token = '6156031628:AAET2m_0JsGDWEdZau-7k0B7Zr36rCj0lB4'

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def greeting(message):
    markup = types.InlineKeyboardMarkup()
    menu_button = types.InlineKeyboardButton("Меню", callback_data='menu')
    markup.add(menu_button)
    text = f'Здравствуй, {message.from_user.first_name}\nЗдесь ты можешь узнать гороскоп по знаку'
    return bot.send_message(message.chat.id, text, reply_markup=markup)


def menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    horoscope_button = types.InlineKeyboardButton('Классический гороскоп', callback_data='horoscope')
    markup.add(horoscope_button)
    text = f'Выбери подходящий вариант'
    return bot.send_message(chat_id, text, reply_markup=markup)


def accept_sign(message):
    try:
        sign_id = Sign.get_sign_by_translated_name(message.text)[0]
        print(sign_id)
        horoscope_info = scrap_horoscope_today_by_sign(sign_id)
    except Exception as e:
        print(e)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = call.data.split('_')
    command = data[0]
    chat_id = call.message.chat.id
    if command == 'menu':
        menu(chat_id)
    elif command == 'horoscope':
        bot_message = bot.send_message(chat_id=call.message.chat.id, text='Напиши название знака зодиака на русском языке')
        bot.register_next_step_handler(message=bot_message, callback=accept_sign)


bot.polling(none_stop=True)

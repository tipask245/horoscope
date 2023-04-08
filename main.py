import telebot
from telebot import types
from models.signs import Sign
from scraper.scraper import *

token = '6156031628:AAET2m_0JsGDWEdZau-7k0B7Zr36rCj0lB4'

bot = telebot.TeleBot(token)

menu_button = types.InlineKeyboardButton('Меню', callback_data='menu')


@bot.message_handler(commands=['start'])
def greeting(message):
    markup = types.InlineKeyboardMarkup()
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
        sign_id, sign_name, translated_name = Sign.get_sign_by_translated_name(message.text)
        if not sign_id or not sign_name:
            return
        markup = types.InlineKeyboardMarkup()
        horoscope_ru_button = types.InlineKeyboardButton('Гороскоп на русском', callback_data=f'hru_{sign_name}_{translated_name}')
        horoscope_en_button = types.InlineKeyboardButton('Гороскоп на английском', callback_data=f'hen_{sign_id}_{sign_name}')
        markup.add(horoscope_ru_button)
        markup.add(horoscope_en_button)
        chat_id = message.chat.id
        return bot.send_message(chat_id=chat_id, text='Выбери подходящий язык', reply_markup=markup)
    except Exception as e:
        print(e)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = call.data.split('_')
    command = data[0]
    chat_id = call.message.chat.id
    markup = types.InlineKeyboardMarkup()
    if command == 'menu':
        menu(chat_id)
    elif command == 'horoscope':
        bot_message = bot.send_message(chat_id=chat_id, text='Напиши название знака зодиака на русском языке')
        bot.register_next_step_handler(message=bot_message, callback=accept_sign)
    elif command == 'hru':
        horoscope_info = scrap_horoscope_today_by_sign_ru(data[1])
        print(horoscope_info)
    elif command == 'hen':
        main_horoscope, matches, mood = scrap_horoscope_today_by_sign_en(data[1])
        main_text = f'*{data[2]}*\n\n{main_horoscope}\n\n{matches}\n{mood}'
        markup.add(menu_button)
        bot.send_message(chat_id=chat_id, text=main_text, reply_markup=markup, parse_mode='Markdown')
    bot.answer_callback_query(call.id)


bot.polling(none_stop=True)

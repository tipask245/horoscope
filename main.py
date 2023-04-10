import telebot
from telebot import types
from models.signs import Sign
from models.history import History
from scraper.scraper import *
from datetime import datetime, timedelta


token = '6156031628:AAET2m_0JsGDWEdZau-7k0B7Zr36rCj0lB4'

bot = telebot.TeleBot(token)

menu_button = types.InlineKeyboardButton('Меню', callback_data='menu')


@bot.message_handler(commands=['start'])
def greeting(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(menu_button)
    text = f'Здравствуй, {message.from_user.first_name}\nЗдесь ты можешь узнать гороскоп по знаку'
    return bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)


def menu(chat_id: int):
    markup = types.InlineKeyboardMarkup()
    horoscope_button = types.InlineKeyboardButton('Классический/китайский гороскоп по знаку', callback_data='horoscope')
    history_button = types.InlineKeyboardButton('История', callback_data='history')
    markup.add(horoscope_button)
    markup.add(history_button)
    text = f'Выбери подходящий вариант'
    return bot.send_message(chat_id, text, reply_markup=markup)


def send_options(chat_id: int, sign_name: str, sign_num: int, translated_name: str, horoscope_type: str):
    markup = types.InlineKeyboardMarkup()
    if horoscope_type == 'cl':
        horoscope_ru_button = types.InlineKeyboardButton('Гороскоп на русском',
                                                         callback_data=f'hru_{sign_name}_{translated_name}')
        horoscope_en_button = types.InlineKeyboardButton('Гороскоп на английском',
                                                         callback_data=f'hen_{sign_num}_{sign_name}')
    else:
        horoscope_ru_button = types.InlineKeyboardButton('Китайский гороскоп на русском',
                                                         callback_data=f'сh-hru_{sign_name}_{translated_name}')
        horoscope_en_button = types.InlineKeyboardButton('Китайский гороскоп на английском',
                                                         callback_data=f'сh-hen_{sign_num}_{sign_name}')
    markup.add(horoscope_ru_button)
    markup.add(horoscope_en_button)
    markup.add(menu_button)
    return bot.send_message(chat_id=chat_id, text=f'*{translated_name}*\n\nВыбери подходящий язык', reply_markup=markup,
                            parse_mode='Markdown')


def accept_sign(message):
    try:
        sign = Sign.get_sign_by_translated_name(message.text)
        sign_num, sign_name, translated_name, horoscope_type = sign[0], sign[1], sign[2], sign[3]
        if not sign_num or not sign_name:
            return
        chat_id = message.chat.id
        user_id = message.from_user.id
        History.add_history_note(user_id=user_id, sign_name=sign_name)
        return send_options(chat_id=chat_id, sign_num=sign_num, sign_name=sign_name, translated_name=translated_name,
                            horoscope_type=horoscope_type)
    except Exception as e:
        print(f'Ошибка: {type(e)} => {e}')


def add_horoscope_buttons(command: str, sign_num: int, sign_name: str, markup: types.InlineKeyboardMarkup):
    markup.add(types.InlineKeyboardButton('Вчерашний', callback_data=f'{command}-yesterday_{sign_num}_{sign_name}'))
    markup.add(types.InlineKeyboardButton('На сегодня', callback_data=f'{command}-today_{sign_num}_{sign_name}'))
    markup.add(types.InlineKeyboardButton('На завтра', callback_data=f'{command}-tomorrow_{sign_num}_{sign_name}'))
    markup.add(types.InlineKeyboardButton('На неделю', callback_data=f'{command}-weekly_{sign_num}_{sign_name}'))
    markup.add(types.InlineKeyboardButton('На месяц', callback_data=f'{command}-monthly_{sign_num}_{sign_name}'))


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = call.data.split('_')
    command = data[0]
    chat_id = call.message.chat.id
    markup = types.InlineKeyboardMarkup()
    if command == 'menu':
        menu(chat_id)
    elif command == 'history':
        user_id = call.from_user.id
        notes = History.get_notes_by_user_id(user_id)
        for note in notes:
            sign_num, sign_name, translated_name, horoscope_type = note[0], note[1], note[2], note[3]
            sign_button = types.InlineKeyboardButton(translated_name, callback_data=f'hstr-sign_{sign_num}_{sign_name}_'
                                                                                    f'{translated_name}_{horoscope_type}')
            markup.add(sign_button)
        markup.add(menu_button)
        bot.send_message(chat_id=chat_id, text='История' if notes else 'История пустая', reply_markup=markup)
    elif command == 'hstr-sign':
        sign_num, sign_name, translated_name, horoscope_type = data[1], data[2], data[3], data[4]
        send_options(chat_id=chat_id, sign_num=sign_num, sign_name=sign_name, translated_name=translated_name,
                     horoscope_type=horoscope_type)
    elif command == 'horoscope':
        bot_message = bot.send_message(chat_id=chat_id, text='Напиши название знака зодиака на русском языке')
        bot.register_next_step_handler(message=bot_message, callback=accept_sign)
    elif command == 'hru':
        today = datetime.today().strftime("%d-%m-%Y")
        yesterday = datetime.today() - timedelta(days=1)
        tomorrow = datetime.today() + timedelta(days=1)
        markup.add(types.InlineKeyboardButton('Вчерашний', callback_data=f'hru-{yesterday.strftime("%d-%m-%Y")}_{data[1]}_{data[2]}'))
        markup.add(types.InlineKeyboardButton('На сегодня', callback_data=f'hru-{today}_{data[1]}_{data[2]}'))
        markup.add(types.InlineKeyboardButton('На завтра', callback_data=f'hru-{tomorrow.strftime("%d-%m-%Y")}_{data[1]}_{data[2]}'))
        markup.add(menu_button)
        bot.send_message(chat_id=chat_id, text='Выбери нужное время', reply_markup=markup)
    elif command in ('hen', 'сh-hen'):
        add_horoscope_buttons(command=command, sign_num=data[1], sign_name=data[2], markup=markup)
        markup.add(menu_button)
        bot.send_message(chat_id=chat_id, text='Выбери нужное время', reply_markup=markup)
    elif command[:4] == 'hru-':
        interval = command[4:]
        date, main_horoscope = scrap_horoscope_by_sign_name_ru(sign_name=data[1], interval=interval)
        main_text = f'*{data[2]}, {date}*\n\n{main_horoscope}'
        markup.add(menu_button)
        bot.send_message(chat_id=chat_id, text=main_text, reply_markup=markup, parse_mode='Markdown')
    elif command[:4] == 'hen-':
        interval = command[4:]
        main_horoscope, matches, mood = scrap_horoscope_by_sign_num_en(sign_num=data[1], interval=interval)
        main_text = f'*{data[2]}*\n\n{main_horoscope}\n\n{matches}\n{mood}'
        markup.add(menu_button)
        bot.send_message(chat_id=chat_id, text=main_text, reply_markup=markup, parse_mode='Markdown')
    elif command == 'сh-hru':
        sign_name, translated_name = data[1], data[2]
        markup.add(types.InlineKeyboardButton('Вчерашний', callback_data=f'{command}-yesterday_{sign_name}_{translated_name}'))
        markup.add(types.InlineKeyboardButton('На сегодня', callback_data=f'{command}-today_{sign_name}_{translated_name}'))
        markup.add(types.InlineKeyboardButton('На завтра', callback_data=f'{command}-tomorrow_{sign_name}_{translated_name}'))
        markup.add(types.InlineKeyboardButton('На неделю', callback_data=f'{command}-week_{sign_name}_{translated_name}'))
        markup.add(types.InlineKeyboardButton('На месяц', callback_data=f'{command}-month_{sign_name}_{translated_name}'))
        markup.add(menu_button)
        bot.send_message(chat_id=chat_id, text='Выбери нужное время', reply_markup=markup)
    elif command[:7] == 'сh-hen-':
        interval = command[7:]
        main_horoscope = scrap_ch_horoscope_by_sign_num_en(sign_num=data[1], interval=interval)
        main_text = f'*{data[2]}*\n\n{main_horoscope}'
        markup.add(menu_button)
        bot.send_message(chat_id=chat_id, text=main_text, reply_markup=markup, parse_mode='Markdown')
    elif command[:7] == 'сh-hru-':
        interval = command[7:]
        title, main_horoscope = scrap_ch_horoscope_by_sign_name_ru(sign_name=data[1], interval=interval)
        main_text = f'*{data[2]}*\n\n{title}\n\n{main_horoscope}'
        markup.add(menu_button)
        bot.send_message(chat_id=chat_id, text=main_text, reply_markup=markup, parse_mode='Markdown')

    bot.answer_callback_query(call.id)


bot.polling(none_stop=True)

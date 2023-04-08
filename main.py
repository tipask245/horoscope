import telebot
from telebot import types
from models.signs import Sign

token = '6156031628:AAET2m_0JsGDWEdZau-7k0B7Zr36rCj0lB4'

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def greeting(message):
    inline_markup = types.InlineKeyboardMarkup()
    menu_button = types.InlineKeyboardButton("Меню", callback_data='menu')
    inline_markup.add(menu_button)
    text = f'Здравствуй, {message.from_user.first_name}\nЗдесь ты можешь узнать гороскоп по знаку'
    return bot.send_message(message.chat.id, text, reply_markup=inline_markup)


bot.polling(none_stop=True)

import telebot
from telebot import types

token = ''

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def greeting(message):
    inline_markup = types.InlineKeyboardMarkup()
    menu_button = types.InlineKeyboardButton("Меню", callback_data='menu')
    text = f''
    return bot.send_message(message.chat.id, text, reply_markup=inline_markup)


bot.polling(none_stop=True)

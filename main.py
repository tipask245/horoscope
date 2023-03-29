import telebot

token = ''

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def greeting(message):
    text = f''
    return bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)

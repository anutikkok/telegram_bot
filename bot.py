import config
import telebot
import db

# Настраиваем соединение с нашим ботом
bot = telebot.TeleBot(config.token)

#Бот отвечает на команды
@bot.message_handler(commands = ['start'])
def send_welcome(message):
    query = "SELECT info_com FROM commands WHERE id = 1"
    result = db.query(query)
    bot.reply_to(message, result)

@bot.message_handler(commands = ['help'])
def send_welcome(message):
    query = "SELECT info_com FROM commands WHERE id = 2"
    result = db.query(query)
    bot.reply_to(message,result)
#Бот отвечает на все сообщения по умолчанию
def echo_all(message):
    bot.reply_to(message, message.text)

#Запускаем бота
bot.polling()




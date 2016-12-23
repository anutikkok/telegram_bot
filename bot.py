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
def send_help(message):
    query = "SELECT info_com FROM commands WHERE id = 2"
    result = db.query(query)
    bot.reply_to(message, result)

#Бот отвечает на все сообщения по умолчанию
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    zap = "SELECT grouping_data FROM address_street WHERE address_street.grouping_data LIKE '%"+ message.text +"%'"
    result_zap = db.query(zap)
    print(result_zap)
    if result_zap == []:
        pope = "SELECT address_street.grouping_data FROM address_street WHERE address_street.name LIKE '%" + message.text + "%' OR address_street.name LIKE '%" + message.text.title() + "%' OR address_street.city LIKE '%" + message.text + "%' OR address_street.city LIKE '%" + message.text.title() + "%'"
        result = db.query(pope)
        if result == []:
            query = "SELECT info_com FROM commands WHERE id = 3"
            result = db.query(query)
            bot.reply_to(message, result)
        else:
            for i in range(len(result)):
                bot.reply_to(message, result[i])
    else:
        zap_id = "SELECT address_street.id FROM address_street WHERE address_street.grouping_data LIKE '%" + message.text + "%'"
        result_zap_id = str(db.query(zap_id))
        pope = "SELECT address_build.number FROM address_build WHERE address_build.street_id = '%" + result_zap_id + "%'"
        result = db.query(pope)
        print("Вывод домов", result)
        for i in range(len(result)):
            bot.reply_to(message, result[i])




#Запускаем бота
bot.polling(none_stop=True, interval=0)
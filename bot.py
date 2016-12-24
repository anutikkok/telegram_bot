import config
import telebot
import db
from telebot import types
# Настраиваем соединение с нашим ботом
bot = telebot.TeleBot(config.token)

#Получение chat_id
upd = bot.get_updates()
last_upd = upd[-1]
message_from_user = last_upd.message
chat_id = message_from_user.chat.id

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
#chat_id = 275266392

chat_id = message_from_user.chat.id

#Бот отвечает на все сообщения по умолчанию
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    select_street_query = "SELECT DISTINCT grouping_data FROM address_street WHERE address_street.grouping_data LIKE '%"+ message.text +"%' OR address_street.grouping_data LIKE '%"+ message.text.title() +"%' "
    street_list = db.query(select_street_query)
    if len(street_list) > 50:
        query = "SELECT info_com FROM commands WHERE id = 4"
        result = db.query(query)
        bot.reply_to(message, result)
    else:
        if street_list == []:
            query = "SELECT info_com FROM commands WHERE id = 3"
            result = db.query(query)
            bot.reply_to(message, result)
        else:
            # TODO: Выводим список улиц по совпадению, только необходимо не сообщениями, а клавиатурой
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            i = 1
            while i == 1:
                for street in street_list:
                    markup.row(street)
                bot.send_message(message.chat.id, "Продолжим:", reply_markup=markup)
                i = 0
            str_list = message.text
            select_street_id = "SELECT address_street.id FROM address_street WHERE address_street.grouping_data LIKE '" + str_list + "'"
            street_id = db.query(select_street_id) # Запрос на выборку id улицы
            for id in street_id:
                pope = "SELECT address_build.number FROM address_build WHERE address_build.street_id = " + str(id)
                result2 = db.query(pope)
                f = open("itog.txt", "w")
                for res in result2:
                    #bot.reply_to(message, res)
                    f.write('д.' + str(res) + ', ' + str(str_list) + '; \n\n')
                keyboard_hider = types.ReplyKeyboardHide()
                bot.send_message(message.chat.id, 'Вы можете скачать файл. Спасибо за то, что с нами. Приятной работы.', reply_markup=keyboard_hider)
                f.close()
                f = open("itog.txt", "r")
                bot.send_document(message.chat.id, f)
                f.close()




    # TODO: Необходимо создать клавиатуру
    # TODO: От клавиатуры получим точное название улицы, после чего выбираем дома
    # TODO: Реализуйте это, и я Вам засчитаю бота:)

#Запускаем бота
bot.polling(none_stop=True, interval=0)
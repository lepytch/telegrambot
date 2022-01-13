import telebot, traceback
from config import *
from extensions import APIException, Convertor


token = TOKEN
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет ✌️ Нужна помощь? - введи "
                                      "/help; список доступных валют - /values")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Для получения актуальной информации по курсам валют, "
                                      "введи название валюты, которую нужно перевести, название "
                                      "в которую перевести и количество. Пример: евро доллар 5. "
                                      "Для получения списка доступных валют, введи команду /values.")


@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def Converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.infinity_polling()

import telebot
import traceback
from extensions import APIException, Convertor
from config import TOKEN, currency


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.chat.id, f"Привет, {message.chat.username} \n"
                                      f"Хочешь узнать курс нужной тебе валюты? \n"
                                      f"Отправь мне сообщение вида: \n"
                                      f"рубль доллар(направление обмена) 100(объем обмена) \n"
                                      f"Чтобы узнать список доступных валют отправь /values")

@bot.message_handler(commands=['values'])
def values(message):
    text = "Доступные валюты:"
    for i in currency.keys():
        text = "\n".join((text, i))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split()
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.send_message(message.chat.id, f"Неизвестная ошибка:\n{e}")
    else:
        bot.send_message(message.chat.id, answer)


bot.polling()

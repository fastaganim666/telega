import telebot
from config import TOKEN, VALUTA
from extensions import Converter, ConversionException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message):
    bot.reply_to(message, 'Формат ввода:\n [валюта, цену которой нужно узнать] '
                          '[в какой валюте] [количетсво первой валюты]\n'
                          '/values - список доступных валют')


@bot.message_handler(commands=['values'])
def valuta(message):
    text = 'Доступные валюты:'
    for key in VALUTA.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConversionException('Введите 3 параметра. Пример: \nдоллар рубль 100')
        quote, base, amount = list(map(str.lower, values))
        total = Converter.get_price(quote, base, amount)
    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n {e}')
    else:
        bot.reply_to(message, f'Цена {amount} {quote} составляет {total:.2f} {base}')


bot.polling(none_stop=True)

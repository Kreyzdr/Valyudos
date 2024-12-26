import telebot

from checking_for_correctness import ConvertionException, CryptoConverter # импортируем обработчик ошибок
from argument import TOKEN, currency # импортируем токен и валюты для бота

bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=["start", "help"])
def help(massage):
    """
Сообщение предназначено для информирования о том, как вводить свои запросы, а также для предложения посмотреть доступные валюты.

Оно приходит в следующих случаях:
1. Пользователь только зашел и нажимает /start (или сам пишет).
2. Пользователь написал /help.
     """
    bot.send_message(massage.chat.id, "Чтобы узнать стоимость валюты введите команду боту:")
    bot.send_message(massage.chat.id, "<имя валюты> , <в какую валюту перевести> , <количество переводимой валюты>")
    bot.send_message(massage.chat.id, "Чтобы узнать весь доступный список валют:   /values")



@bot.message_handler(commands=['values'])
def out_currencies(massage):
    """
    Если пользователь ввел /values, отобразится список доступных валют.
    Я хотел сделать листами, чтобы пользователь мог сначала посмотреть первую половину, а потом вторую,
     дабы не перегружать его монотонным текстом. Однако список оказался не таким большим,
      поэтому не было смысла реализовывать эту идею.
    """
    text = 'Доступная валюта:'

    for key in currency.keys():
        text = '\n'.join((text, key))
    bot.send_message(massage.chat.id, text)



@bot.message_handler(content_types=['text'])
def convert(message):
    """
    Обрабатывает запрос на конвертацию криптовалюты.

    Параметры:
    message (Message): Объект сообщения с текстом формата "base,quote,amount".

    Исключения:
    - ConvertionException: Если передано неверное количество параметров (должно быть 3).
    - Exception: Для любых других ошибок (например, ошибки сервера).

    Возвращаемое значение:
    Сообщение с результатом конвертации или сообщение об ошибке.

    Пример: "USD,EUR,100" конвертирует 100 USD в EUR.
    """
    value = message.text.split(',')
    try:

        if len(value) != 3:
            raise ConvertionException('Много/мало параметров было передано боту')

        base, quote, amount = value
        result = CryptoConverter.convert(base, quote, amount)

    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя. \n {e}")

    except Exception as e:
        bot.reply_to(message, f"Ошибка на сервере. {e}")

    else:
        bot.reply_to(message, f'''Цена {base} {quote} в {amount}: {float(result) * float(amount)}''')



bot.polling(non_stop=True)

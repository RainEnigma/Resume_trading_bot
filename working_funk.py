import go_back_to_main
from config import config


def get_data():
    forming_string = '*Валюта   Своб.   Использ.   Всего\n*'
    balance = config.kuna().fetch_balance()
    currency_list = ['USD', 'UAH', 'BTC', 'ETH', 'WAVES']

    for currency in currency_list:
        forming_string = f'{forming_string}\n' \
                         f'*{currency}*' \
                         f'       {round(balance.get(currency).get("free"),4)}' \
                         f'       {round(balance.get(currency).get("used"),4)}' \
                         f'       {round(balance.get(currency).get("total"),4)}'
    return forming_string


def kurse_waves(currency):
    forming_string = f'Курс {currency} на сегодня:\n'
    forming_string = f'{forming_string}\n' \
                     f'сейчас   - {config.kuna().fetch_ticker("WAVES/UAH").get("last")}\n' \
                     f'максимум - {config.kuna().fetch_ticker("WAVES/UAH").get("high")}\n' \
                     f'минимум  - {config.kuna().fetch_ticker("WAVES/UAH").get("low")}\n\n' \
                     f'Сейчас продают  - {config.kuna().fetch_ticker("WAVES/UAH").get("ask")}\n' \
                     f'Сейчас покупают - {config.kuna().fetch_ticker("WAVES/UAH").get("bid")}'
    return forming_string


def what_sdelka(message, bot):
    if message.text == '🔝 На главную':
        go_back_to_main.go_back_to_main(message, 'Мы в главном меню!')
    else:
        bot.send_message(message.from_user.id,
                         sdelki(message.text),
                         parse_mode='markdown')
        go_back_to_main.go_back_to_main(message, 'Мы в главном меню!')


def sdelki(argum=1):
    try:
        argum = int(argum)
    except Exception:
        argum = 1
    forming_answer = []
    last_sdelka = len(config.kuna().fetch_my_trades('WAVES/UAH')) - argum
    id = config.kuna().fetch_my_trades('WAVES/UAH')[last_sdelka].get('id')
    curr = config.kuna().fetch_my_trades('WAVES/UAH')[last_sdelka].get('symbol')
    side = config.kuna().fetch_my_trades('WAVES/UAH')[last_sdelka].get('side')
    price = config.kuna().fetch_my_trades('WAVES/UAH')[last_sdelka].get('price')
    skolko = config.kuna().fetch_my_trades('WAVES/UAH')[last_sdelka].get('amount')
    costs = config.kuna().fetch_my_trades('WAVES/UAH')[last_sdelka].get('cost')
    forming_string = f'*{id}*\n\n' \
                     f'валюта - {curr}\n' \
                     f'операция - {side}\n' \
                     f'стоимость - {price}грн.\n' \
                     f'сколько - {skolko}waves\n' \
                     f'в грн - {costs}грн.'

    forming_answer.append(forming_string)
    return forming_answer


def buy_currency(message, bot):
    if message.text == '🔝 На главную':
        go_back_to_main.go_back_to_main(message, 'мы в главном меню!')
    else:
        # купить number вейвов

        try:
            config.kuna().create_market_buy_order('WAVES/UAH', message.text)
            bot.send_message(message.from_user.id, f'Мы купили {message.text} WAVES')
        except Exception as e:
            bot.send_message(message.from_user.id, f'ОШИБКА!!!\n{e}')


def auto_buy_currency(bot, number):
    # купить number вейвов

    try:
        config.kuna().create_market_buy_order('WAVES/UAH', number)
        bot.send_message(config.list_admins[0], f'Мы купили {number} WAVES')
    except Exception as e:
        bot.send_message(config.list_admins[0], f'ОШИБКА!!!\n{e}')


def auto_sell_currency(bot, number):
    # купить number вейвов

    try:
        config.kuna().create_market_sell_order('WAVES/UAH', number)
        bot.send_message(config.list_admins[0], f'Мы продали {number} WAVES')
    except Exception as e:
        bot.send_message(config.list_admins[0], f'ОШИБКА!!!\n{e}')


def sell_currency(message, bot):
    if message.text == '🔝 На главную':
        go_back_to_main.go_back_to_main(message, 'мы в главном меню!')
    else:
        # продать number вейвов
        try:
            config.kuna().create_market_sell_order('WAVES/UAH', message.text)
            bot.send_message(message.from_user.id, f'Мы продали {message.text} WAVES')
        except Exception as e:
            bot.send_message(message.from_user.id, f'ОШИБКА!!!\n{e}')

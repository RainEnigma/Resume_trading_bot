import WorkCurrency
import working_funk
from config import config


def start_job1(bot):
    config.kuna().fetch_balance().get('WAVES').get('free')
    price_buy_last = config.kuna().fetch_my_trades('WAVES/UAH')[
        len(config.kuna().fetch_my_trades('WAVES/UAH')) - 1].get(
        'price')
    selling_now = config.kuna().fetch_ticker('WAVES/UAH').get('bid')
    balance_UAH = config.kuna().fetch_balance().get('UAH').get('free')
    print(selling_now)
    print(price_buy_last)
    print(price_buy_last * 0.99)

    try:
        if selling_now < price_buy_last * 0.99:
            working_funk.auto_buy_currency(bot, balance_UAH * 0.997)
            bot.send_message(238008205, 'Купили WAVES!')
    except Exception:
        pass


def start_job(bot):
    balance_WAVES = config.kuna().fetch_balance().get('WAVES').get('free')
    free_UAH = config.kuna().fetch_balance().get('UAH').get('free')
    high_curse = config.kuna().fetch_ticker("WAVES/UAH").get("high")
    low_curse = config.kuna().fetch_ticker("WAVES/UAH").get("low")
    price_buy_last = config.kuna().fetch_my_trades('WAVES/UAH')[
        len(config.kuna().fetch_my_trades('WAVES/UAH')) - 1].get('price')
    selling_now = config.kuna().fetch_ticker('WAVES/UAH').get('ask')
    buying_now = config.kuna().fetch_ticker('WAVES/UAH').get('bid')
    balance_UAH = config.kuna().fetch_balance().get('UAH').get('free')
    # print(f'selling_now = {selling_now}')
    # print(f'low_curse = {low_curse}')
    # print(f'low_curse +10% = {low_curse * 1.01}')


    # print(f'if seling_now ({selling_now}) < low_curse+1%({low_curse * 1.01})')
    print(f'if seling_now ({selling_now}) < price_buy_last+1%({price_buy_last * 1.01})')
    print()
    print(f'if buying_now ({buying_now}) > high_curse-1%({high_curse * 0.99})')
    print()

    # print(f'buying_now = {buying_now}')
    print(f'balance_UAH - {balance_UAH}')
    # print(balance_UAH * 0.996)
    # can_buy_in_WAVES = format((balance_UAH / selling_now) * 0.9974, '.8f')
    can_buy_in_WAVES = WorkCurrency.WorkCurrency('UAH').can_buy()

    can_sell_WAVES = format(balance_WAVES * 0.9974, '.8f')
    print(f'can_buy_in_WAVES - {can_buy_in_WAVES}')
    print(f'can_sell_WAVES - {can_sell_WAVES}')
    # print(price_buy_last)
    # print(price_buy_last * 0.99)
    side = config.kuna().fetch_my_trades('WAVES/UAH')[len(config.kuna().fetch_my_trades('WAVES/UAH')) - 1].get('side')
    print(side)
    ###
    balance = config.kuna().fetch_balance()
    cbn = balance.get("UAH").get("free")
    sell_now = config.kuna().fetch_ticker("WAVES/UAH").get("ask")  # сейчас продают
    in_waves_sans_comission = cbn / sell_now * 0.8
    ###
    if side == 'sell':

        try:
            if selling_now < low_curse * 1.01:
                working_funk.auto_buy_currency(bot, in_waves_sans_comission)
                # working_funk.auto_buy_currency(bot, can_buy_in_WAVES)
                # bot.send_message(238008205, 'Купили WAVES!')
        except Exception:
            pass
    if side == 'buy':
        try:
            # if buying_now > high_curse * 0.99:
            if buying_now > price_buy_last * 1.01:
                working_funk.auto_sell_currency(bot, can_sell_WAVES)
        except Exception:
            pass

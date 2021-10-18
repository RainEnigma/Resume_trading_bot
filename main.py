from datetime import datetime

import telebot
from telebot import types

import WorkCurrency
import thread_start_func
import working_funk
from config import config
from database import func_for_creating_tables, add_user_to_table
from from_exel_file import text_message
from keyboards import keyboards

bot = telebot.TeleBot(config.API_TOKEN, threaded=True)

# запуск ф-ции для создания таблиц в базе данных
func_for_creating_tables.func_creating_tables()


@bot.message_handler(commands=['start'])
def start(message, marker=None):
    if message.from_user.id in config.list_admins:
        # Добавление нового пользователя в таблицу
        for tab_name in ['USERS']:
            add_user_to_table.add_user_to_table_HM(tab_name,
                                                   user_id=message.from_user.id,
                                                   user_name=str(message.from_user.username),
                                                   last_name=str(message.from_user.last_name),
                                                   name=str(message.from_user.first_name),
                                                   date_add=str(datetime.now().date()))

        if marker is None:
            bot.send_sticker(message.chat.id, open(config.path_image_logo, 'rb'))
            bot.send_message(message.chat.id,
                             f"{text_message(1, 1)}",
                             reply_markup=keyboards.start_keyboard(message))
        else:
            bot.send_message(message.chat.id,
                             marker,
                             reply_markup=keyboards.start_keyboard(message))
    else:
        bot.send_message(message.from_user.id, 'Извините это приватный бот!')


@bot.message_handler(commands=['help'])
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_start = types.KeyboardButton("/start")
    markup.row(button_start)
    bot.send_message(message.chat.id,
                     text_message(2, 1),
                     reply_markup=markup, parse_mode='markdown')


@bot.message_handler(content_types=['text'])
def func_1(message):
    if message.text == '🔝 На главную':
        import go_back_to_main
        go_back_to_main.go_back_to_main(message)

    elif message.text == '📈 баланс' and message.from_user.id in config.list_admins:
        bot.send_message(message.from_user.id,
                         str(working_funk.get_data()),
                         parse_mode='markdown')

    elif message.text == '💸 Курс валют' and message.from_user.id in config.list_admins:
        bot.send_message(message.from_user.id,
                         str(working_funk.kurse_waves('WAVES/UAH')),
                         parse_mode='markdown')

    elif message.text == 'сделки' and message.from_user.id in config.list_admins:
        bot.send_message(message.from_user.id,
                         'Отправь какую сделку показать (номер с конца!)',
                         parse_mode='markdown',
                         reply_markup=keyboards.go_to_main_keyboard(message))

        bot.register_next_step_handler(message, working_funk.what_sdelka, bot)


    elif message.text == 'купить WAVES' and message.from_user.id in config.list_admins:

        bot.send_message(message.from_user.id,
                         f"у нас есть {config.kuna().fetch_balance().get('UAH').get('free')} грн. сколько"
                         f" WAWES берем?\n"
                         f"*КУРС - {config.kuna().fetch_ticker('WAVES/UAH').get('ask')}*",
                         parse_mode='markdown',
                         reply_markup=keyboards.go_to_main_keyboard(message))
        bot.register_next_step_handler(message, working_funk.buy_currency, bot)


    elif message.text == 'продать WAVES' and message.from_user.id in config.list_admins:
        bot.send_message(message.from_user.id,
                         f"у нас есть {config.kuna().fetch_balance().get('WAVES').get('free')} WAVES сколько продадим?"
                         f"\n*КУРС - {config.kuna().fetch_ticker('WAVES/UAH').get('bid')}*",
                         parse_mode='markdown',
                         reply_markup=keyboards.go_to_main_keyboard(message))
        bot.register_next_step_handler(message, working_funk.sell_currency, bot)

    elif message.text == 'test' and message.from_user.id in config.list_admins:
        answer = WorkCurrency.WorkCurrency('WAVES').now_curse()
        answer = WorkCurrency.WorkCurrency('UAH').can_buy()
        bot.send_message(message.from_user.id,
                         answer,
                         parse_mode='markdown',
                         reply_markup=keyboards.go_to_main_keyboard(message))
        bot.register_next_step_handler(message, working_funk.sell_currency, bot)




    else:
        bot.send_message(message.from_user.id, 'Непонiмать 🤷‍♂️')


# def run_threaded():
#     job_thread = threading.Thread(target=schedule_job.job(bot), name='auto_trade')
#     job_thread.start()
#
# schedule.every(1).seconds.do(run_threaded)
#
# def main_loop():
#
#     bot.infinity_polling(none_stop=True)
#     while 1:
#         schedule.run_pending()
#         time.sleep(1)


if __name__ == '__main__':
    try:
        bot.infinity_polling(none_stop=True)

    except Exception as e:
        print(f"bot_poling - {e}")

try:
    from schedule_job import start_job

    thread_start_func.set_interval(start_job, config.interval_search_for_trades, bot)
except Exception as e:
    print(f"problem in buying cash - {e}")

#
# while True:
#     schedule.run_pending()
#     time.sleep(1)

from telebot import types

from config import config


def start_keyboard(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['💸 Курс валют']])

    if message.from_user.id in config.list_admins:
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['📈 баланс', 'сделки']])
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['купить WAVES', 'продать WAVES']])
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['🔑 Администрирование', 'test']])

    return keyboard


def go_to_main_keyboard(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['🔝 На главную']])

    return keyboard

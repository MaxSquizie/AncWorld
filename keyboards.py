from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton

kb_1 = [[types.KeyboardButton(text="Да"), types.KeyboardButton(text="Нет")]]
confirm_keyboard = types.ReplyKeyboardMarkup(keyboard=kb_1, resize_keyboard=True)

kb_2 = [[types.KeyboardButton(text="Человек"), types.KeyboardButton(text="Эльф"), types.KeyboardButton(text="Гном")],
        [types.KeyboardButton(text="Нежить"), types.KeyboardButton(text="Орк"), types.KeyboardButton(text="Халфлинг")]]
race_keyboard = types.ReplyKeyboardMarkup(keyboard=kb_2, resize_keyboard=True)

kb_3 = [[types.KeyboardButton(text="Принять"), types.KeyboardButton(text="Назад")]]

apply_menu = types.ReplyKeyboardMarkup(keyboard=kb_3, resize_keyboard=True)

set_menu = InlineKeyboardMarkup(row_width=1,
                                inline_keyboard=[
                                        [InlineKeyboardButton(
                                                text="Персонаж",
                                                callback_data='char'
                                        ),
                                        InlineKeyboardButton(
                                                text="Умения",
                                                callback_data='skills'
                                        )],
                                        [InlineKeyboardButton(
                                                text="Профессии",
                                                callback_data='profs'
                                        ),
                                        InlineKeyboardButton(
                                                text="Закрыть",
                                                callback_data='closed'
                                        )],
                                ])

char_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                        [InlineKeyboardButton(
                                                text="Сумка",
                                                callback_data='bag'
                                        )],
                                        [InlineKeyboardButton(
                                                text="Экипировка",
                                                callback_data='equipment'
                                        )],
                                        [InlineKeyboardButton(
                                                text="Питомец",
                                                callback_data='pet'
                                        )],
                                        [InlineKeyboardButton(
                                                text="Артефакты",
                                                callback_data='arts'
                                        )],
                                        [InlineKeyboardButton(
                                                text="Назад",
                                                callback_data='menu'
                                        ),
                                        InlineKeyboardButton(
                                                text="Закрыть",
                                                callback_data='closed'
                                        )]
                                ])


def quest_button(i):
        return InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(
                text=f"Квест",
                callback_data=f'{i}'
        )],])



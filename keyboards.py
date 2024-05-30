from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
import datas as dt
from typing import Optional

kb_1 = [[types.KeyboardButton(text="Да"), types.KeyboardButton(text="Нет")]]
confirm_keyboard = types.ReplyKeyboardMarkup(keyboard=kb_1, resize_keyboard=True)

kb_2 = [[types.KeyboardButton(text="Человек"), types.KeyboardButton(text="Эльф"), types.KeyboardButton(text="Гном")],
        [types.KeyboardButton(text="Нежить"), types.KeyboardButton(text="Орк"), types.KeyboardButton(text="Халфлинг")]]
race_keyboard = types.ReplyKeyboardMarkup(keyboard=kb_2, resize_keyboard=True)

kb_3 = [[types.KeyboardButton(text="Принять"), types.KeyboardButton(text="Назад")]]

apply_menu = types.ReplyKeyboardMarkup(keyboard=kb_3, resize_keyboard=True)


set_menu = InlineKeyboardMarkup(row_width=2,
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
                                        ),
                                        InlineKeyboardButton(
                                                text="Экипировка",
                                                callback_data='equipment'
                                        )],
                                        [InlineKeyboardButton(
                                                text="Питомец",
                                                callback_data='pet'
                                        ),
                                        InlineKeyboardButton(
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

skill_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                        [InlineKeyboardButton(
                                                text="Навыки",
                                                callback_data='ability'
                                        ),
                                        InlineKeyboardButton(
                                                text="Характеристики",
                                                callback_data='characteristic'
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



def quest_button(i, parameter: Optional[InlineKeyboardButton], PCQ=None) -> Optional[InlineKeyboardMarkup]:
        if not (PCQ is None):
                if parameter is None:
                        return InlineKeyboardMarkup(row_width=1, inline_keyboard=[
                        [InlineKeyboardButton(
                                text=f"Сдать квест",
                                callback_data=f"complete {i}"
                        )],])
                else:
                        return InlineKeyboardMarkup(row_width=1, inline_keyboard=[
                                [InlineKeyboardButton(
                                        text=f"Сдать квест",
                                        callback_data=f"complete {i}"
                                )], ].append(parameter))
        elif not (parameter is None):
                return InlineKeyboardMarkup(row_width=1, inline_keyboard=[
                [InlineKeyboardButton(
                        text=f"Квест",
                        callback_data=f'{i}'
                )],].append(parameter))
        else:
                return InlineKeyboardMarkup(row_width=1, inline_keyboard=[
                        [InlineKeyboardButton(
                                text=f"Квест",
                                callback_data=f'{i}'
                        )], ])


def carousel_menu(char):
        if char.get_temp() > 1 and char.get_temp() < len(dt.commodity):
                return InlineKeyboardMarkup(row_width=3,
                                        inline_keyboard=[
                                                [InlineKeyboardButton(
                                                        text="⬅️",
                                                        callback_data='left'
                                                ),
                                                InlineKeyboardButton(
                                                        text="Купить",
                                                        callback_data='buy'
                                                ),
                                                InlineKeyboardButton(
                                                        text="➡️",
                                                        callback_data='right'
                                                )]]
                                        )
        elif char.get_temp() > 1 and char.get_temp() >= len(dt.commodity):
                return InlineKeyboardMarkup(row_width=3,
                                     inline_keyboard=[
                                             [InlineKeyboardButton(
                                                     text="⬅️",
                                                     callback_data='left'
                                             ),
                                                     InlineKeyboardButton(
                                                             text="Купить",
                                                             callback_data='buy'
                                                     ),
                                             InlineKeyboardButton(
                                                     text="⬛️",
                                                     callback_data="⬛"
                                             )]]
                                     )
        elif char.get_temp() <= 1 and char.get_temp() < len(dt.commodity):
                return InlineKeyboardMarkup(row_width=3,
                                     inline_keyboard=[
                                             [InlineKeyboardButton(
                                                     text="⬛",
                                                     callback_data="⬛"
                                             ),
                                             InlineKeyboardButton(
                                                     text="Купить",
                                                     callback_data='buy'
                                             ),
                                             InlineKeyboardButton(
                                                     text="➡️",
                                                     callback_data="right"
                                             )]]
                                     )
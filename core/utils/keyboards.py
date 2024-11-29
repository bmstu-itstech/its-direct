from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from core.text.text import btn

def get_admin_keyboard() -> types.InlineKeyboardMarkup:
    raise NotImplemented

'''
get_first_statement_button - функция для вызова кнопки подачи заявления
'''
def get_first_statement_button() -> types.ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(KeyboardButton(btn.make_ticket))
    return keyboard

'''
get_type_of_statement_keyboard - функция для вызова клавиатуры выбора типа заявления
Вопросы - question
Проблема - problem
Предложение - suggestion
'''
def get_type_of_statement_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(KeyboardButton(btn.question),
                 KeyboardButton(btn.problem),
                 KeyboardButton(btn.suggestion),
                 KeyboardButton(btn.back))
    return keyboard

'''
get_category_of_statement_keyboard - Функция для вызова инлайн клавиатуры для выбора категории
обращения, каждая инлайн кнопка со своим запросом
'''
def get_category_of_statement_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    keyboard.add(KeyboardButton(btn.study),
                 KeyboardButton(btn.hostel),
                 KeyboardButton(btn.food),
                 KeyboardButton(btn.medicine),
                 KeyboardButton(btn.army),
                 KeyboardButton(btn.army),
                 KeyboardButton(btn.documents),
                 KeyboardButton(btn.money),
                 KeyboardButton(btn.electives),
                 KeyboardButton(btn.other),
                 KeyboardButton(btn.back),
                 )
    return keyboard

def get_anonim_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(KeyboardButton(btn.yes),
                 KeyboardButton(btn.no),
                 KeyboardButton(btn.back))
    return keyboard

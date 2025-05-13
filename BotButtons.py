from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


action_bar = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Новий чат')]
])


def models_kb(ollama_list):
    kb = InlineKeyboardBuilder()
    for i in list(ollama_list)[0][1]:
        i_ = list(i)[0][1]
        kb.button(text=i_, callback_data=f"model:{i_}")

    return kb.as_markup()

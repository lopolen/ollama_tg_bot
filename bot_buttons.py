from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

action_bar = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Новий чат')]
])


def models_kb(ollama_list):
    kb = InlineKeyboardBuilder()
    for i in list(ollama_list)[0][1]:
        i_ = list(i)[0][1]
        kb.button(text=i_, callback_data=f"model:{i_}")

    return kb.as_markup()

import asyncio
import logging
import sys
import os

from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import ollama

import BotButtons


load_dotenv()
bot_key = os.getenv('BOT_KEY')

dp = Dispatcher()


user_chosen_model = {}
chat_history = {}


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"{message.from_user.id}", reply_markup=BotButtons.action_bar)


@dp.message(F.text == 'Новий чат')
async def command_new_chat_handler(message: Message) -> None:
    await message.answer('Оберіть модель ШІ:', reply_markup=BotButtons.models_kb(ollama.list()))


@dp.callback_query(F.data.startswith('model:'))
async def model_chosen_handler(callback: CallbackQuery) -> None:
    await callback.answer(f"Модель {callback.data[6:]} завантажено. Починіть розмову")
    user_chosen_model[callback.from_user.id] = callback.data[6:]
    chat_history[callback.from_user.id] = None


@dp.message()
async def chat_handler(message: Message) -> None:
    user_id = message.from_user.id
    if user_id in user_chosen_model.keys():
        user_message = {'role': 'user', 'content': message.text}

        if chat_history[user_id] is not None:
            chat_history[user_id].append(user_message)
        else:
            chat_history[user_id] = [user_message]

        response = ollama.chat(model=user_chosen_model[user_id],
                               messages=chat_history[user_id])
        print(chat_history)
        chat_history[user_id].append(dict(response.message))

        await message.answer(response.message.content)

    else:
        await message.answer("Спочатку оберіть модель")


async def main() -> None:
    bot = Bot(token=bot_key, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

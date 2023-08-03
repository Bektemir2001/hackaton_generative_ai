import time
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from env import TOKEN

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)


class UserState(StatesGroup):
    CHOOSING = State()


# Инициализация словаря для хранения выбора пользователя
memory = {}


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    logging.info(f'{user_id} {time.asctime()}')

    await message.reply(f"Hi, {user_name} !!!!!\nвведите текст:")


@dp.message_handler(state=None)
async def message_handler(message: types.Message):
    await message.reply(f"Вот исправленный текст\n\n{message.text}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)





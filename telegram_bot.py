import time
import logging
from aiogram import Bot, Dispatcher, executor, types
from env import TOKEN
from model import correcctor_txt
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    logging.info(f'{user_id} {time.asctime()}')

    await message.reply(f"Hi, {user_name} !!!!!\nвведите текст:")


@dp.message_handler(state=None)
async def message_handler(message: types.Message):
    correct_txt = correcctor_txt(message.text)
    await message.reply(f"Вот исправленный текст\n\n{correct_txt}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)





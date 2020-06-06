# The telegram bot server that runs directly

from aiogram import Bot, Dispatcher, executor, types
import logging

import commands
import re
import patterns
from tokens import API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Sends a welcome message and help on the bot"""
    await message.answer(
        "Bot for accounting for finances\n\n"
        "Add a wall newspaper element: /add\n"
        "Generate a wall newspaper: /generate\n"
    )


@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def add_element(message: types.Message):
    cmd = ''
    try:
        cmd = str(message.caption)
    except KeyError:
        pass

    match = re.match(patterns.ADDPIC, cmd)
    if match:
        caption = cmd[5:]
        image = message.photo[-1]

        f_path = await image.get_file()
        f_path = f_path['file_path']

        # TODO raise exceptions
        commands.add_person_picture(f_path, message.chat.id, caption)

        await message.answer('Done 👌')


@dp.message_handler(commands=['gen', 'generate'])
async def generate_news_paper(message: types.Message):
    chat_id = message.chat.id
    # TODO ... generate photo
    await bot.send_photo(chat_id, open('./output/output.jpg', 'rb'), 'Done 👌')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

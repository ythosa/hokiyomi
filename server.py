# The telegram bot server that runs directly

from aiogram import Bot, Dispatcher, executor, types
import re
import logging

import commands
from exceptions import InvalidAttachments
import patterns
from tokens import API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Sends a welcome message and help on the bot"""
    await message.answer(
        "Cute & funny bot for creating a wall newspaper with your friends\n\n"
        "Add a wall newspaper element: /add\n"
        "Generate a wall newspaper: /generate\n"
        "Remove last added element: /remove_last\n"
    )


@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def add_element(message: types.Message):
    """Add element to db for creating wall newspaper then"""
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

        try:
            commands.add_person_picture(f_path, message.chat.id, caption)
        except InvalidAttachments as e:
            await message.answer(str(e))

        await message.answer('Done 👌')


@dp.message_handler(commands=['rvlast', 'remove_last'])
async def remove_last_element(message: types.Message):
    """Remove last added element from db"""
    commands.remove_last(message.chat.id)
    await message.answer('Done 👌')


@dp.message_handler(commands=['gen', 'generate'])
async def generate_news_paper(message: types.Message):
    """Send generated wall newspaper"""
    chat_id = message.chat.id
    # TODO ... generate photo
    await bot.send_photo(chat_id, open('./output/output.jpg', 'rb'), 'Have fun :3')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

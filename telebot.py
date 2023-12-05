from aiogram import Bot, Dispatcher
from aiogram.types.input_file import BufferedInputFile
import asyncio
from config import bot_token, chat_id


async def send_message(msgText=list):
    bot = Bot(token=bot_token)
    if len(msgText[0]) > 4000:
        msgText[0] = msgText[0][0:3999]
    await bot.send_message(
        chat_id=chat_id,
        text=msgText[0],
    )
    await asyncio.sleep(3)
    await bot.session.close()
    if len(msgText) > 1:
        await send_attach(msgText[1][1], msgText[1][0])
    return True


async def send_attach(filename, document):
    bot = Bot(token=bot_token)
    doc = BufferedInputFile(file=document, filename=filename)
    obj = await bot.send_document(
        chat_id, doc)
    await asyncio.sleep(2)
    await bot.session.close()

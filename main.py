import traceback
from mail_reader import checkMail
from telebot import send_message
import asyncio
from logger import logger


async def main():
    try:
        claim = await checkMail()
        if claim:
            try:
                await send_message(claim)
            except Exception as e:
                await (send_message([traceback.format_exc()]))
    except Exception as e:
        logger(str(traceback.format_exc()))
    await asyncio.sleep(0.5)


if __name__ == '__main__':
    while True:
        asyncio.run(main())

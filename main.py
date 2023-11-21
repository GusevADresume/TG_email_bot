from mail_reader import checkMail
from telebot import send_message
import asyncio


async def main():
    try:
        claim = checkMail()
        if claim:
            try:
                await send_message(claim)
            except:
                await (send_message(['!!!!!!!Something is wrong in bot part, check your email!!!!!!!']))
    except:
        await (send_message(['!!!!!!!Something is wrong in email, check your email!!!!!!!']))
    await asyncio.sleep(2)


if __name__ == '__main__':
    while True:
        asyncio.run(main())

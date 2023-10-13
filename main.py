import asyncio
import sys
from os import getenv

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiohttp import BasicAuth
from bot import dp, logger
from bot.handlers import register_all_handlers


async def main():
    logger.info("Start app")
    auth = BasicAuth(login=getenv("PROXY_USER"), password=getenv("PROXY_PASS"))
    session = AiohttpSession(proxy=(getenv("PROXY_HOST"), auth))
    bot = Bot(token=getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML, session=session)
    register_all_handlers(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":

    asyncio.run(main())

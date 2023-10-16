import asyncio
from asyncio import CancelledError
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiohttp import BasicAuth
from sqlite_fsm_storage import AioSQLiteStorage

from bot import logger, form_router
from bot.handlers import register_all_handlers


async def main():
    logger.info("Start app")
    auth = BasicAuth(login=getenv("PROXY_USER"), password=getenv("PROXY_PASS"))
    session = AiohttpSession(proxy=(getenv("PROXY_HOST"), auth))
    storage = AioSQLiteStorage()
    await storage.start()
    dp = Dispatcher(storage=storage)
    dp.include_router(form_router)
    bot = Bot(token=getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML, session=session)
    register_all_handlers(dp)
    try:
        await dp.start_polling(bot, allowed_updates=['message', 'callback_query'])
    except CancelledError:
        pass
    finally:
        await bot.session.close()
        await storage.close()


if __name__ == "__main__":

    asyncio.run(main())

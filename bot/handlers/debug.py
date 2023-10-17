import logging

from aiogram.types import CallbackQuery

from bot import form_router

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# @form_router.callback_query()
# async def handle_all_callback_queries(callback_query: CallbackQuery):
#     # Логируем входящую callback_query
#     logger.info(f"Received callback_query: {callback_query.data}")

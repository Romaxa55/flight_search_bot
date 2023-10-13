from aiogram.types import CallbackQuery
from bot import dp, logger


# @dp.callback_query(lambda c: True)
# async def handle_callback_query(callback_query: CallbackQuery):
#     logger.info(f"Received callback query from {callback_query.from_user.first_name}: {callback_query.data}")
#     await callback_query.answer()  # Не забудьте ответить на callback query, даже если вы не отправляете никакого уведомления

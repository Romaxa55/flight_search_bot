from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery
)
from aiogram3_calendar import SimpleCalendar, simple_cal_callback

from bot import form_router, BookingForm
from bot.keybords import Keyboards
from bot.utils import CurrencyInfo


async def nav_cal_handler(message: Message):
    await message.edit_text("Укажите дату вылета: ", reply_markup=await SimpleCalendar().start_calendar())


# simple calendar usage
@form_router.callback_query(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    print(date)
    # if selected:
    #     await callback_query.message.answer(
    #         f'You selected {date.strftime("%d/%m/%Y")}', reply_markup=Keyboards.calendar_keyboard()
    #     )



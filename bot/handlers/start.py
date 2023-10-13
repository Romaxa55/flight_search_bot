from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from bot import form_router, BookingForm
from bot.utils import CurrencyInfo


@form_router.message(CommandStart())
async def start_booking(message: Message, state: FSMContext) -> None:
    await state.set_state(BookingForm.preferred_currency.state)
    currencies = CurrencyInfo.get_currencies()

    buttons = [
        [
            InlineKeyboardButton(text=f"{flag} {symbol}", callback_data=currency_code)
            for currency_code, (symbol, flag) in chunk
        ]
        for chunk in CurrencyInfo.chunks(list(currencies.items()), 8)
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Добро пожаловать! Пожалуйста, введите предпочитаемую валюту для бронирования.",
                         reply_markup=keyboard)

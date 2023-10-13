from typing import Any

from aiogram.filters import CommandStart, MagicData
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton, CallbackQuery
)

from bot import form_router, BookingForm, logger, dp
from bot.utils import CurrencyInfo


@form_router.message(CommandStart())
async def start_booking(message: Message, state: FSMContext) -> None:
    await state.set_state(BookingForm.preferred_currency)

    currencies = CurrencyInfo.get_currencies()

    buttons = [
        [
            InlineKeyboardButton(text=f"{flag} {symbol}", callback_data=f"currency_{currency_code}")
            for currency_code, (symbol, flag) in chunk
        ]
        for chunk in CurrencyInfo.chunks(list(currencies.items()), 3)
        # Уменьшил количество кнопок в ряду до 3 для удобства
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Добро пожаловать! Пожалуйста, выберите предпочитаемую валюту для бронирования.",
                         reply_markup=keyboard)


@form_router.callback_query(lambda c: c.data.startswith('currency_'))
async def handle_currency(callback_query: CallbackQuery):
    currency_code = callback_query.data.split('_')[1]
    await callback_query.message.answer(f"Выбрана валюта: {currency_code}")



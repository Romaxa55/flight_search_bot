from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton, CallbackQuery
)

from bot import form_router, BookingForm
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

    await message.answer("Пожалуйста, выберите предпочитаемую валюту для бронирования.",
                         reply_markup=keyboard)


@form_router.callback_query(lambda c: c.data.startswith('currency_'))
async def handle_currency(callback_query: CallbackQuery, state: FSMContext):
    currency_code = callback_query.data.split('_')[1]
    await callback_query.message.edit_text(f"Выбрана валюта: {currency_code}")
    await state.update_data(currency=currency_code)


@form_router.message(Command("show_profile"))
async def get_currency(message: Message, state: FSMContext):
    data = await state.get_data()
    currency = data.get('currency')
    if currency:
        await message.answer(f"Ваша текущая валюта: {currency}")
    else:
        await message.answer("Вы не выбрали валюту.")

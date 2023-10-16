from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery
)

from bot import form_router, BookingForm
from bot.keybords import Keyboards
from bot.utils import CurrencyInfo


@form_router.message(CommandStart())
async def start_booking(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    current_currency = user_data.get('currency')
    await state.set_state(BookingForm.preferred_currency)

    if current_currency:
        await message.answer(f"Ваша текущая валюта: {current_currency}. Хотите изменить?",
                             reply_markup=Keyboards.change_currency_keyboard())
    else:
        await message.answer("Пожалуйста, выберите предпочитаемую валюту для бронирования.",
                             reply_markup=Keyboards.currency_selection_keyboard(
                                 CurrencyInfo.get_currencies()
                             ))


@form_router.callback_query(lambda c: c.data.startswith('currency_'))
async def handle_currency(callback_query: CallbackQuery, state: FSMContext):
    currency_code = callback_query.data.split('_')[1]
    await callback_query.message.edit_text(f"Выбрана валюта: {currency_code}")
    await state.update_data(currency=currency_code)


@form_router.callback_query(lambda c: c.data == "confirm_change_currency")
async def confirm_change_currency(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Пожалуйста, выберите новую предпочитаемую валюту.")
    await callback_query.message.edit_reply_markup(reply_markup=Keyboards.currency_selection_keyboard(
        CurrencyInfo.get_currencies()
    ))
#
#
# @form_router.callback_query("cancel_change_currency")
# async def cancel_change_currency(callback_query: CallbackQuery):
#     await callback_query.message.edit_text("Выбор валюты отменен.")
#     await callback_query.message.edit_reply_markup()  # Удалить клавиатуру


@form_router.message(Command("show_profile"))
async def get_currency(message: Message, state: FSMContext):
    data = await state.get_data()
    currency = data.get('currency')
    if currency:
        await message.answer(f"Ваша текущая валюта: {currency}")
    else:
        await message.answer("Вы не выбрали валюту.")

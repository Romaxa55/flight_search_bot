import asyncio
import logging
import sys
from os import getenv
from typing import Any, Dict

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

TOKEN = getenv("BOT_TOKEN")

form_router = Router()


class BookingForm(StatesGroup):
    preferred_currency = State()
    departure_city = State()
    arrival_city = State()
    travel_dates = State()
    number_of_people = State()
    city_options = State()
    flight_options = State()
    booking_details = State()
    payment = State()


@form_router.message(CommandStart())
async def start_booking(message: Message, state: FSMContext) -> None:
    await state.set_state(BookingForm.preferred_currency.state)
    await message.answer("Добро пожаловать! Пожалуйста, введите предпочитаемую валюту для бронирования.")


@form_router.message(BookingForm.preferred_currency)
async def process_currency(message: Message, state: FSMContext) -> None:
    await state.update_data(preferred_currency=message.text)
    await state.set_state(BookingForm.departure_city.state)
    await message.answer("Понял вас! Теперь, откуда вы будете вылетать?")


@form_router.message(BookingForm.departure_city)
async def process_departure_city(message: Message, state: FSMContext) -> None:
    await state.update_data(departure_city=message.text)
    await state.set_state(BookingForm.arrival_city.state)
    await message.answer("Отлично! Куда вы хотели бы полететь?")


@form_router.message(BookingForm.arrival_city)
async def process_arrival_city(message: Message, state: FSMContext) -> None:
    await state.update_data(arrival_city=message.text)
    await state.set_state(BookingForm.travel_dates.state)
    await message.answer("Идеально! Теперь укажите даты вашей поездки и количество человек.")

@form_router.message(BookingForm.travel_dates)
async def process_travel_dates(message: Message, state: FSMContext) -> None:
    await state.update_data(travel_dates=message.text)
    await state.set_state(BookingForm.city_options.state)
    await message.answer("Теперь, пожалуйста, выберите города вылета и прилёта из следующих вариантов: ...")


@form_router.message(BookingForm.city_options)
async def process_city_options(message: Message, state: FSMContext) -> None:
    await state.update_data(city_options=message.text)
    await state.set_state(BookingForm.flight_options.state)
    await message.answer("Вот доступные рейсы. Пожалуйста, выберите один: ...")


@form_router.message(BookingForm.flight_options)
async def process_flight_options(message: Message, state: FSMContext) -> None:
    await state.update_data(flight_options=message.text)
    await state.set_state(BookingForm.booking_details.state)
    await message.answer("Вот детали вашего бронирования. Пожалуйста, подтвердите для перехода к оплате.")


@form_router.message(BookingForm.booking_details)
async def process_booking_details(message: Message, state: FSMContext) -> None:
    await state.update_data(booking_details=message.text)
    await state.set_state(BookingForm.payment.state)
    await message.answer("Спасибо за подтверждение! Пожалуйста, перейдите к оплате, перейдя по следующей ссылке: ...")


@form_router.message(BookingForm.payment)
async def process_payment(message: Message, state: FSMContext) -> None:
    await state.update_data(payment=message.text)
    await state.clear()
    await message.answer("Ваше бронирование завершено! Спасибо, что выбрали нас для своих путешествий.")


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

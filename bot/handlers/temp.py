from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery
)
from aiogram3_calendar import simple_cal_callback, SimpleCalendar
from .. import dp, form_router, BookingForm


@dp.callback_query(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}',
        )


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

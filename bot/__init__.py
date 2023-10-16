import logging

from aiogram import Router
from aiogram.fsm.state import State, StatesGroup

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

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


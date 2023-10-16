from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.utils import CurrencyInfo


class Keyboards:

    @staticmethod
    def change_currency_keyboard():
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Изменить валюту", callback_data="confirm_change_currency"),
                    InlineKeyboardButton(text="Отмена", callback_data="cancel_change_currency")
                ]
            ]
        )

    @staticmethod
    def currency_selection_keyboard(currencies):
        buttons = [
            [
                InlineKeyboardButton(text=f"{flag} {symbol}", callback_data=f"currency_{currency_code}")
                for currency_code, (symbol, flag) in chunk
            ]
            for chunk in CurrencyInfo.chunks(list(currencies.items()), 3)
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)

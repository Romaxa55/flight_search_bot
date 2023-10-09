class CurrencyInfo:
    @staticmethod
    def get_currencies():
        return {
            "USD": ("$", "🇺🇸"),
            "EUR": ("€", "🇪🇺"),
            "GBP": ("£", "🇬🇧"),
            "JPY": ("¥", "🇯🇵"),
            "CNY": ("¥", "🇨🇳"),
            "RUB": ("₽", "🇷🇺"),
        }

    @staticmethod
    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]


def format_flight_data(flight_data):
    # TODO: Форматирование данных о рейсе для отправки пользователю
    pass

def send_message(user_id, message):
    # TODO: Отправка сообщения пользователю
    pass

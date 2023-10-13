import pkgutil
import importlib
from aiogram import Dispatcher


def register_all_handlers(dp: Dispatcher):
    # Импортируем все модули в текущем пакете
    for _, module_name, _ in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f"{__name__}.{module_name}")
        # Предполагаем, что каждый модуль имеет функцию register_handlers(dp)
        if hasattr(module, "register_handlers"):
            module.register_handlers(dp)

import logging
from time import perf_counter
from types import FunctionType, MethodType

from app.constants import DATETIME_FORMAT, FILE_LOGGER, FORMAT_LOGGER

logging.basicConfig(
    format=FORMAT_LOGGER,
    level=logging.INFO,
    datefmt=DATETIME_FORMAT,
    filename=FILE_LOGGER,
    filemode='w'
)
logger = logging.getLogger('Планировщик')


def notify(func, *args, **kwargs):
    """
    Логгирует начало и конец выполнения исходной функции
    и возвращает новую функцию, инкапсулирующую поведение
    исходной функции
    """
    def func_composite(*args, **kwargs):
        # Обычная функциональность notify
        logger.info(f'Начинаю {func.__doc__.lower()}')
        start = perf_counter()
        result = func(*args, **kwargs)
        if result is None:
            logger.error(f'{func.__doc__} завершилось ошибкой')
        else:
            finish = perf_counter()
            logger.info(
                f'Закончил {func.__doc__.lower()}. '
                f'Выполнение заняло {round(finish-start, 4)} сек.'
            )
        return result
    # Возврат сложной функции
    return func_composite


class Notifies(type):
    """
    Метакласс, меняющий поведение своих классов
    на новые методы, 'дополненные' поведением
    преобразователя сложной функции notify()
    """
    def __new__(cls, name, bases, attr):
        for name, value in attr.items():
            if type(value) is FunctionType or type(value) is MethodType:
                attr[name] = notify(value)
        return super(Notifies, cls).__new__(cls, name, bases, attr)

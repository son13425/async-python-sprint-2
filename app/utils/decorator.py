from functools import wraps
from app.loggs.logger import logger


def coroutine(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            gen = f(*args, **kwargs)
            gen.send(None)
            return gen
        except StopIteration:
            logger.error('Генератор не создан')

    return wrap

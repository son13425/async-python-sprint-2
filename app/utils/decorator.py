from functools import wraps
from typing import Callable, Generator, Optional, Any


def coroutine(func: Callable) -> Generator[Optional[Any], None, None]:
    """Декоратор инициализирует генератор"""
    @wraps(func)
    def wrap(
        *args: Any,
        **kwargs: Any
    ) -> Generator[Optional[Any], None, None]:
        generator = func(*args, **kwargs)
        generator.send(None)
        return generator
    return wrap()

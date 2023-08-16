import time
from datetime import datetime
from typing import Callable, List, Optional
from uuid import uuid4


class Job:
    """Задача"""
    def __init__(
        self,
        target: Callable,
        args: tuple = None,  # type: ignore
        kwargs: dict = None,  # type: ignore
        job_uid: Optional[str] = None,
        start_at: Optional[datetime] = None,      # время запуска
        max_working_time: int = -1,               # длительность выполнения
        tries: int = 0,                           # количество рестартов
        dependencies: Optional[List] = []         # зависимости
    ) -> None:
        self.args = args or ()
        self.kwargs = kwargs or {}
        self.coroutine = target(*self.args, **self.kwargs)
        self.job_uid = job_uid if job_uid else uuid4().hex
        self.target = target
        self.start_at = start_at
        self.max_working_time = max_working_time
        self.tries = tries
        self.dependencies = dependencies

    def run(self) -> None:
        self.coroutine.send(self.job_uid)

    def pause(self, time_pause: int):
        time.sleep(time_pause)

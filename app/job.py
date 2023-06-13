from uuid import uuid4
from datetime import datetime
from typing import Optional, List, Tuple, Any, Generator


class Job:
    """Задача"""
    def __init__(
        self,
        target: Generator[Optional[Any], None, None],
        args: Optional[Tuple[Any, ...]] = None,
        job_uid: Optional[str] = None,
        start_at: Optional[datetime] = None,      # время запуска
        max_working_time: int = -1,               # длительность выполнения
        tries: int = 0,                           # количество рестартов
        dependencies: Optional[List[str]] = None  # зависимости
    ) -> None:
        self.__args = args or ()
        self.__coroutine = target(*self.__args)
        self.job_uid = job_uid if job_uid else uuid4().hex
        self.start_at = start_at
        self.max_working_time = max_working_time
        self.tries = tries
        self.dependencies = dependencies

    def run(self) -> None:
        self.__coroutine.send(None)

    def pause(self):
        pass

    def stop(self):
        pass

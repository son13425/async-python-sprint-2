from queue import Queue
from datetime import datetime as dt
from threading import Timer, Condition, Thread
from typing import List
from app.job import Job
from app.loggs.logger import logger
from time import perf_counter


condition = Condition()
work_list = []


class Scheduler:
    """Планировщик задач"""
    def __init__(self, pool_size: int) -> None:
        self.__queue: Queue[Job] = Queue()
        self.pool_size: int = pool_size

    def schedule(self, task: Job) -> None:
        Thread(target=self.is_time, args=(task, condition, work_list)).start()
        with condition:
            condition.wait_for(lambda: len(work_list) == 1)
            if all(work_list):
                self.__queue.put(task)
                logger.info(
                    f'Задача {task.job_uid} - "{task.target.__doc__}" '
                    'отправлена в очередь'
                )
        self.run()

    def run(self) -> None:
        while not self.__queue.empty():
            job = self.__queue.get()
            logger.info(
                f'Задача {job.job_uid} - "{job.target.__doc__}" '
                'получена из очереди'
            )
            try:
                job.run()

            except StopIteration:
                continue
            finally:
                logger.info(
                    f'Задача {job.job_uid} - "{job.target.__doc__}" выполнена'
                )

    def restart(self):
        pass

    def stop(self):
        pass

    def is_time(self, task: Job, condition: Condition, work_list: List) -> None:
        with condition:
            time_current = perf_counter()
            if task.start_at is not None and time_current > task.start_at:
                logger.info(
                    f'Задача {task.job_uid} - "{task.target.__doc__}" '
                    'остановлена: время запуска прошло'
                )
                work_list.append(False)
            else:
                if task.start_at is not None and time_current < task.start_at:
                    time_pause = round(task.start_at - time_current, 0)
                    logger.info(
                        f'Задача {task.job_uid} - "{task.target.__doc__}" '
                        f'на паузе на {time_pause} секунд'
                    )
                    task.pause(time_pause)
                    work_list.append(True)
            condition.notify()

    def time_is_up(self, task: Job, condition: Condition, work_list: List) -> None:
        with condition:
            pass

    def is_tries(self, task: Job, condition: Condition, work_list: List) -> None:
        with condition:
            pass

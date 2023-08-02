from queue import Queue
from threading import Condition, Thread
from typing import List
from app.job import Job
from app.loggs.logger import logger
from time import perf_counter
from app.log_status.log_status import record_status_log


condition = Condition()
work_list = []


class Scheduler:
    """Планировщик задач"""
    def __init__(self, pool_size: int) -> None:
        self.__queue: Queue[Job] = Queue()
        self.pool_size: int = pool_size

    def schedule(self, task: Job) -> None:
        record_status_log.overwrite_job_status(task.job_uid, 'START')
        Thread(target=self.is_time, args=(task, condition, work_list)).start()
        with condition:
            condition.wait_for(lambda: len(work_list) == 1)
            if all(work_list):
                self.__queue.put(task)
                record_status_log.overwrite_job_status(
                    task.job_uid,
                    'IN_QUEUE'
                )
                logger.info(
                    f'Задача {task.job_uid} - "{task.target.__doc__}" '
                    'отправлена в очередь'
                )
        self.run()

    def run(self) -> None:
        while not self.__queue.empty():
            job = self.__queue.get()
            record_status_log.overwrite_job_status(job.job_uid, 'IN_PROGRESS')
            logger.info(
                f'Задача {job.job_uid} - "{job.target.__doc__}" '
                'получена из очереди'
            )
            try:
                job.run()
            except StopIteration:
                continue

    def restart(self):
        pass

    def stop(self):
        pass

    def is_time(
            self, task: Job, condition: Condition, work_list: List
    ) -> None:
        with condition:
            time_current = perf_counter()
            if task.start_at is None:
                work_list.append(True)
            elif task.start_at is not None and time_current > task.start_at:
                record_status_log.overwrite_job_status(
                    task.job_uid,
                    'ABORTED'
                )
                logger.info(
                    f'Задача {task.job_uid} - "{task.target.__doc__}" '
                    'остановлена: время запуска прошло'
                )
                work_list.append(False)
            else:
                if task.start_at is not None and time_current < task.start_at:
                    time_pause = round(task.start_at - time_current, 0)
                    record_status_log.overwrite_job_status(
                        task.job_uid,
                        'PAUSE'
                    )
                    logger.info(
                        f'Задача {task.job_uid} - "{task.target.__doc__}" '
                        f'на паузе на {time_pause} секунд'
                    )
                    task.pause(time_pause)
                    work_list.append(True)
            condition.notify()

    def time_is_up(
        self, task: Job, condition: Condition, work_list: List
    ) -> None:
        with condition:
            pass

    def is_tries(
        self, task: Job, condition: Condition, work_list: List
    ) -> None:
        with condition:
            pass

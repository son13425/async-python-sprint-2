from queue import Queue
from threading import Condition, Thread
from typing import List
from app.job import Job
from app.loggs.logger import logger
from time import perf_counter
from app.log_status.log_status import record_status_log
import concurrent.futures as pool
from app.constants import FILE_STATUS_LOG
import json


class Scheduler:
    """Планировщик задач"""
    def __init__(self, pool_size: int) -> None:
        self.__queue: Queue[Job] = Queue()
        self.pool_size: int = pool_size

    def schedule(self, task: Job) -> bool:
        record_status_log.overwrite_job_status(task.job_uid, 'START')
        condition = Condition()
        work_list = []
        with condition:
            Thread(
                target=self.is_time,
                args=(task, condition, work_list)
            ).start()
            condition.wait()
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
        return True

    def run(self) -> None:
        while not self.__queue.empty():
            job = self.__queue.get()
            logger.info(
                f'Задача {job.job_uid} - "{job.target.__doc__}" '
                'получена из очереди'
            )
            record_status_log.overwrite_job_status(job.job_uid, 'IN_PROGRESS')
            if len(job.dependencies) == 0: # type: ignore
                try:
                    job.run()
                except StopIteration:
                    continue
            else:
                condition = Condition()
                dependencies_list = []
                Thread(
                    target=self.is_dependencies,
                    args=(job, condition, dependencies_list)
                ).start()
                with condition:
                    condition.wait_for(
                        lambda: len(dependencies_list) == len(job.dependencies) # type: ignore
                    )
                    if all(dependencies_list):
                        try:
                            job.run()
                        except StopIteration:
                            continue
                    else:
                        record_status_log.overwrite_job_status(
                            job.job_uid,
                            'ABORTED'
                        )
                        self.restart(job)

    def restart(self, task: Job):
        data = record_status_log.read_status_log()
        for job in data:
            if job['job_uid'] == task.job_uid:
                if job['info_status']['current_tries'] < (
                    job['info_job']['tries']
                ):
                    self.schedule(task)
                    record_status_log.overwrite_job_restart(task.job_uid)
                    logger.info(
                        f'Задача {task.job_uid} - "{task.target.__doc__}" '
                        'рестарт'
                    )
                else:
                    record_status_log.overwrite_job_status(
                        task.job_uid,
                        'ABORTED'
                    )
                    logger.error(
                        f'Задача {task.job_uid} - '
                        f'"{task.target.__doc__}" отменяется: '
                        'закончилось допустимое количество '
                        'рестартов'
                    )
            else:
                continue

    def is_time(
            self, task: Job, condition: Condition, work_list: List
    ) -> None:
        time_current = perf_counter()
        if task.start_at is None:
            work_list.append(True)
        elif task.start_at is not None and time_current > task.start_at: # type: ignore
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
            if task.start_at is not None and time_current < task.start_at: # type: ignore
                time_pause = round(task.start_at - time_current, 0) # type: ignore
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
        with condition:
            condition.notify()

    def is_dependencies(
        self, task: Job, condition: Condition, dependencies_list: list
    ) -> None:
        for job in task.dependencies: # type: ignore
            record_status_log.record_job_status_log(job)
        with condition:
            with pool.ThreadPoolExecutor(
                max_workers=self.pool_size
            ) as executor:
                futures = (
                    [executor.submit(self.schedule, work) for work in task.dependencies] # type: ignore
                )
                for future in pool.as_completed(futures):
                    result = future.result()
                    dependencies_list.append(result)
            condition.notify()

    def time_is_up(
        self, task: Job, condition: Condition, work_list: List
    ) -> None:
        with condition:
            pass

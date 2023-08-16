import concurrent.futures as pool
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from multiprocessing import Process
from queue import Queue
from threading import Condition, Thread
from time import sleep
from typing import List

from app.job import Job
from app.log_status.log_status import record_status_log
from app.loggs.logger import logger


class Scheduler:
    """Планировщик задач"""
    def __init__(self, pool_size: int) -> None:
        self.__queue: Queue[Job] = Queue()
        self.pool_size: int = pool_size

    def schedule(self, task: Job) -> bool:
        """Планирование задачи по времени"""
        record_status_log.overwrite_job_status(task.job_uid, 'START')
        condition = Condition()
        work_list: List[bool] = []
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
        """Выполнение задачи"""
        while not self.__queue.empty():
            job = self.__queue.get()
            logger.info(
                f'Задача {job.job_uid} - "{job.target.__doc__}" '
                'получена из очереди'
            )
            record_status_log.overwrite_job_status(job.job_uid, 'IN_PROGRESS')
            with ThreadPoolExecutor(max_workers=self.pool_size) as pool:
                if job.max_working_time == -1:
                    pool.submit(self.work, job)
                else:
                    process = Process(target=self.work, args=(job, ))
                    process.start()
                    sleep(job.max_working_time)
                    process.terminate()

    def work(self, job: Job):
        """Обработчик"""
        if len(job.dependencies) == 0:  # type: ignore
            try:
                job.run()
            except StopIteration:
                return
        else:
            condition = Condition()
            dependencies_list: List[bool] = []
            Thread(
                target=self.is_dependencies,
                args=(job, condition, dependencies_list)
            ).start()
            with condition:
                condition.wait_for(
                    lambda: len(dependencies_list) == len(
                        job.dependencies  # type: ignore
                    )
                )
                if all(dependencies_list):
                    try:
                        job.run()
                    except StopIteration:
                        return
                else:
                    record_status_log.overwrite_job_status(
                        job.job_uid,
                        'ABORTED'
                    )
                    self.restart(job)

    def restart(self, task: Job):
        """Обработка рестарта"""
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
        """Обработка времени запуска"""
        time_current: datetime = datetime.now()
        if task.start_at is None:
            work_list.append(True)
        elif task.start_at is not None and (
            time_current > task.start_at
        ):
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
            if task.start_at is not None and time_current < (
                task.start_at
            ):
                time_pause = round(
                    (task.start_at - time_current).seconds, 0
                )
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
        """Обработка зависимостей"""
        for job in task.dependencies:  # type: ignore
            record_status_log.record_job_status_log(job)
        with condition:
            with pool.ThreadPoolExecutor(
                max_workers=self.pool_size
            ) as executor:
                futures = (
                    [executor.submit(
                        self.schedule, work
                    ) for work in task.dependencies]  # type: ignore
                )
                for future in pool.as_completed(futures):
                    result = future.result()
                    dependencies_list.append(result)
            condition.notify()

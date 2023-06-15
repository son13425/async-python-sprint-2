from queue import Queue
from threading import Timer, Condition
from app.job import Job
from app.loggs.logger import logger


condition = Condition()


class Scheduler:
    """Планировщик задач"""
    def __init__(self, pool_size: int) -> None:
        self.__queue: Queue[Job] = Queue()
        self.pool_size: int = pool_size

    def schedule(self, task: Job) -> None:
        self.__queue.put(task)
        logger.info(
            f'Задача {task.job_uid} - "{task.target.__doc__}" '
            'отправлена в очередь'
        )

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
        logger.info(
            f'Задача {job.job_uid} - "{job.target.__doc__}" выполнена'
        )

    def restart(self):
        pass

    def stop(self):
        pass

from queue import Queue
from app.constants import MAX_WORKERS
from app.job import Job


class Scheduler:
    """Планировщик задач"""
    def __init__(self, pool_size: int = MAX_WORKERS) -> None:
        self.__queue: Queue[Job] = Queue()

    def schedule(self, task: Job) -> None:
        self.__queue.put(task)

    def run(self) -> None:
        while not self.__queue.empty():
            job = self.__queue.get()
            try:
                job.run()
            except StopIteration:
                continue

    def restart(self):
        pass

    def stop(self):
        pass

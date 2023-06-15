from app.scheduler import Scheduler
from app.constants import MAX_WORKERS
from app.tasks.test_jobs import list_jobs
from threading import Thread
from time import perf_counter
from app.loggs.logger import logger


start = perf_counter()
logger.info('Старт планировщика')
print('Старт планировщика')

threads = []
threads_max = MAX_WORKERS
loop = Scheduler(MAX_WORKERS)

list_tasks = []
for test_job in list_jobs:
    list_tasks.append([loop.schedule(test_job), loop.run()])

for task in list_tasks:
    for job in task:
        thread = Thread(target=job)
        threads.append(thread)
        thread.start()

for thread in threads:
    thread.join()

finish = perf_counter()
print(
    'Все задачи выполнены успешно. '
    f'Выполнение заняло {round(finish-start, 4)} сек.'
)
logger.info(
    'Все задачи выполнены успешно. '
    f'Выполнение заняло {round(finish-start, 4)} сек.'
)

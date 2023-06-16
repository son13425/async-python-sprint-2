from app.scheduler import Scheduler
from app.constants import MAX_WORKERS
from app.tasks.test_jobs import list_jobs
from time import perf_counter, sleep
from app.loggs.logger import logger
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

start = perf_counter()
logger.info('Старт планировщика')
print('Старт планировщика')

threads = []
threads_max = MAX_WORKERS
loop = Scheduler(MAX_WORKERS)

logger.info('Создаем пул для загрузки задач в планировщик')
# with ThreadPoolExecutor(max_workers=threads_max) as pool:
    # for job in list_jobs:
    #     thread = pool.submit(loop.schedule, job)
    #     if job.max_working_time != -1:
    #         sleep(job.max_working_time)
    #         thread.join()
    #         logger.error(
    #             f'Задача {job.job_uid} - "{job.target.__doc__}" '
    #             'прервана: время выполнения истекло'
    #         )

# threads = list(pool.map(loop.schedule, list_jobs))

for job in list_jobs:
    thread = Thread(target=loop.schedule, args=(job, ))
    thread.start()
    if job.max_working_time != -1:
        sleep(job.max_working_time)
        thread.join()
        logger.error(
            f'Задача {job.job_uid} - "{job.target.__doc__}" '
            'прервана: время выполнения истекло'
        )
    thread.join()


finish = perf_counter()
print(
    'Валидные задачи выполнены успешно. '
    f'Выполнение заняло {round(finish-start, 4)} сек.'
)
logger.info(
    'Валидные задачи выполнены успешно. '
    f'Выполнение заняло {round(finish-start, 4)} сек.'
)

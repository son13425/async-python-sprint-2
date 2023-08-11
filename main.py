import json
import os
from app.scheduler import Scheduler
from app.constants import MAX_WORKERS
from app.tasks.test_jobs import list_jobs
from time import perf_counter
from app.loggs.logger import logger
from concurrent.futures import ThreadPoolExecutor
from app.log_status.log_status import record_status_log

from app.constants import FILE_STATUS_LOG


start = perf_counter()
logger.info('Старт планировщика')
print('Старт планировщика')

threads = []
threads_max = MAX_WORKERS
loop = Scheduler(MAX_WORKERS)

# проверяю существование файла журнала текущего состояния планировщика
# если файла нет, то создаю новый
if os.path.exists(FILE_STATUS_LOG) is False:
    logger.error(
        'Внимание! '
        'Файл журнала текущего состояния планировщика '
        f'по адресу {FILE_STATUS_LOG} не найден. '
        'Создан новый файл - исторические данные потеряны'
    )
    FILE_STATUS_LOG.touch(exist_ok=True)
    with open(FILE_STATUS_LOG, 'w', encoding='utf-8') as file:
        file.write('[\n' + ']')


logger.info('Создаем пул для загрузки задач в планировщик')
with ThreadPoolExecutor(max_workers=threads_max) as pool:
    for job in list_jobs:
        job_dict = record_status_log.converting_job_to_dict(job)
        print('job_dict= ', job_dict)
        print()
        status_log = record_status_log.read_status_log()
        print('status_log= ', status_log)
        print()
        in_status_log = False
        if len(status_log) > 0:
            print('len(status_log)= ', len(status_log))
            print()
            for status in status_log:
                print('status= ', status)
                print()
                print(999999)
                print()
                print('job.job_uid= ', job.job_uid)
                print()
                print('status[job_uid]= ', status['job_uid'])
                print()
                if status['info_job'] == job_dict:
                    in_status_log = True
                    print(000)
                    print()
                    if status['info_status']['status'] == 'END':
                        print('000111')
                        print()
                        logger.info(
                            f'Задача {job.job_uid} - '
                            f'"{job.target.__doc__}" завершена ранее'
                        )
                        break
                    elif status['info_status']['current_tries'] <= (
                        status['info_job']['tries']
                    ):
                        print('job.job_uid= ', job.job_uid)
                        print()
                        print('status[job_uid]= ', status['job_uid'])
                        print()
                        record_status_log.overwrite_job_restart(
                            job.job_uid
                        )
                        logger.info(
                            f'Задача {job.job_uid} - '
                            f'"{job.target.__doc__}" повторно '
                            'отправлена в пул задач планировщика'
                        )
                        pool.submit(loop.schedule, job)
                        break
                    else:
                        print(111)
                        print()
                        record_status_log.overwrite_job_status(
                            job.job_uid,
                            'ABORTED'
                        )
                        logger.error(
                            f'Задача {job.job_uid} - '
                            f'"{job.target.__doc__}" отменяется: '
                            'закончилось допустимое количество '
                            'рестартов'
                        )
                        break
            if in_status_log == False:
                print(222)
                print()
                record_status_log.record_job_status_log(job)
                logger.info(
                    f'Задача {job.job_uid} - "{job.target.__doc__}" '
                    'отправлена в пул задач планировщика'
                )
                pool.submit(loop.schedule, job)
                break
        else:
            print(333)
            print()
            record_status_log.record_job_status_log(job)
            logger.info(
                f'Задача {job.job_uid} - "{job.target.__doc__}" '
                'отправлена в пул задач планировщика'
            )
            pool.submit(loop.schedule, job)


finish = perf_counter()
print(
    'Валидные задачи выполнены успешно. '
    f'Выполнение заняло {round(finish-start, 4)} сек.'
)
logger.info(
    'Валидные задачи выполнены успешно. '
    f'Выполнение заняло {round(finish-start, 4)} сек.'
)

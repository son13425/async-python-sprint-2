import json
from threading import Lock

from app.constants import FILE_STATUS_LOG
from app.job import Job


class RecordStatusLog:
    def __init__(self):
        self.lock = Lock()

    def record_job_status_log(self, task: Job):
        """
        Запись новой задачи в журнал
        текущего состояния планировщика
        """
        self.lock.acquire()
        data = {
            'job_uid': task.job_uid,
            'info_job': {
                'target': task.target.__name__,
                'args': str(task.args),
                'kwargs': str(task.kwargs),
                'start_at': str(task.start_at),
                'max_working_time': task.max_working_time,
                'tries': task.tries,
                'dependencies': str(task.dependencies)
            },
            'info_status': {
                'status': 'CREATED',
                'current_tries': 1
            }
        }
        with open(FILE_STATUS_LOG, 'r+', encoding='utf-8') as file:
            s = file.read()
            index = s.rfind(']')
            if index == 2:
                file.seek(index)
                json.dump(data, file, indent=4)
                file.write('\n' + ']')
            else:
                index_n = s.rfind('}')
                file.seek(index_n + 1)
                file.write(',\n')
                json.dump(data, file, indent=4)
                file.write('\n' + ']')
        self.lock.release()

    def read_status_log(self, url):
        """Чтение журнала текущего состояния"""
        self.lock.acquire()
        with open(url, 'r', encoding='utf-8') as file:
            status_log = json.load(file)
            print(status_log)
        self.lock.release()
        return status_log

    def overwrite_job_status(self, job_uid: str, new_status: str):
        """
        Изменение статуса задачи в журнале
        текущего состояния планировщика
        """
        self.lock.acquire()
        with open(FILE_STATUS_LOG, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            for job in data:
                if job['job_uid'] == job_uid:
                    job['info_status']['status'] = new_status
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
        self.lock.release()

    def overwrite_job_restart(self, job_uid: str):
        """
        Изменение текущего количества рестартов в журнале
        текущего состояния планировщика
        """
        self.lock.acquire()
        with open(FILE_STATUS_LOG, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            for job in data:
                if job['job_uid'] == job_uid:
                    job['info_status']['current_tries'] += 1
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
        self.lock.release()

    def converting_job_to_dict(self, job: Job):
        """
        Конвертация информации о задаче
        в словарь
        """
        data = {
            'target': job.target.__name__,
            'args': str(job.args),
            'kwargs': str(job.kwargs),
            'start_at': str(job.start_at),
            'max_working_time': job.max_working_time,
            'tries': job.tries,
            'dependencies': str(job.dependencies)
        }
        return data


record_status_log = RecordStatusLog()

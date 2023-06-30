from app.utils.decorator import coroutine
from urllib.request import urlopen
from http import HTTPStatus
import json
from app.loggs.logger import logger
from app.constants import (
    DATETIME_FORMAT,
    OUTPUT_FILES_DIR
)
import datetime as dt
from app.log_status.log_status import record_status_log


class WorkingNetwork():
    """Работа с сетью"""

    @coroutine
    def get_request(self, url: str) -> str:
        """Get-запрос"""
        output = self.analyze_data()
        job_uid = yield
        with urlopen(url) as response:
            if response.status == HTTPStatus.OK:
                resp_body = response.read().decode("utf-8")
                if resp_body:
                    try:
                        data = json.loads(resp_body)
                    except Exception:
                        record_status_log.overwrite_job_status(
                            job_uid,
                            'ABORTED'
                        )
                        logger.error(
                            f'Задача {job_uid} - Этап '
                            f'"{self.get_request.__doc__}" прервана: '
                            f'по адресу {url} получены невалидные данные'
                        )
                    logger.info(
                        f'Задача {job_uid} - Этап '
                        f'"{self.get_request.__doc__}" выполнена. '
                        'Данные отправлены на обработку'
                    )
                    output.send((job_uid, data))
                    output.close()
            else:
                record_status_log.overwrite_job_status(
                    job_uid,
                    'ABORTED'
                )
                logger.error(
                    f'Задача {job_uid} - Этап "{self.get_request.__doc__}" '
                    f'прервана: задан некорректный адрес {url}'
                )

    @coroutine
    def analyze_data(self):
        """Анализ данных парсинга"""
        output = self.record_item()
        job_uid, data = yield
        if not data:
            record_status_log.overwrite_job_status(
                job_uid,
                'ABORTED'
            )
            logger.error(
                f'Задача {job_uid} - Этап '
                f'"{self.analyze_data.__doc__}" прервана: '
                f'нет данных'
            )
            return
        try:
            item = data['info']
            logger.info(
                f'Задача {job_uid} - Этап '
                f'"{self.analyze_data.__doc__}" выполнена. '
                'Данные отправлены на запись в файл'
            )
            output.send((job_uid, item))
        except GeneratorExit:
            pass

    @coroutine
    def record_item(self):
        """Запись результатов парсинга в файл"""
        job_uid, data = yield
        if not data:
            record_status_log.overwrite_job_status(
                job_uid,
                'ABORTED'
            )
            logger.error(
                f'Задача {job_uid} - Этап '
                f'"{self.record_item.__doc__}" прервана: '
                f'нет данных'
            )
            return
        try:
            OUTPUT_FILES_DIR.mkdir(exist_ok=True)
            now = dt.datetime.now()
            now_formatted = now.strftime(DATETIME_FORMAT)
            file_name = f'{now_formatted}_Результат_парсинга.txt'
            file_path = OUTPUT_FILES_DIR / file_name
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            record_status_log.overwrite_job_status(job_uid, 'END')
            logger.info(
                f'Задача {job_uid} - Этап '
                f'"{self.record_item.__doc__}" выполнена. '
                f'Данные записаны в файл {file_path}'
            )
        except GeneratorExit:
            pass


working_network = WorkingNetwork()

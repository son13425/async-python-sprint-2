import datetime as dt
import os.path
import time
from typing import Any, Generator, Optional
from pathlib import Path

from app.constants import (
    DATETIME_FORMAT,
    OUTPUT_FILES_DIR,
    URL_DEPENDENT
)
from app.loggs.logger import logger
from app.utils.decorator import coroutine
from app.log_status.log_status import record_status_log


class WorkingFiles():
    """Работа с файлами"""

    @coroutine
    def file_create(self, file_path: Path) -> Generator[None, Any, Any]:
        """Создание файла"""
        job_uid = yield
        file_path.touch(exist_ok=True)
        record_status_log.overwrite_job_status(job_uid, 'END')
        logger.info(
            f'Задача {job_uid} - "Зависимость "{self.file_create.__doc__}" '
            'выполнена'
        )

    @coroutine
    def file_read(
        self,
        file_url: Path
    ) -> Generator[None, Any, Any]:
        """Чтeние файла"""
        job_uid = yield
        time.sleep(5)
        if os.path.exists(file_url):
            with open(file_url, encoding='utf-8') as file:
                file.readline()
            record_status_log.overwrite_job_status(job_uid, 'END')
            logger.info(
                f'Задача {job_uid} - "{self.file_read.__doc__}" выполнена'
            )
        else:
            record_status_log.overwrite_job_status(
                job_uid,
                'ABORTED'
            )
            logger.error(
                f'Задача {job_uid} - "{self.file_read.__doc__}" '
                f'прервана: файл для запроса ({file_url}) не найден'
            )

    @coroutine
    def file_output(
        self,
        text: str,
        file_name: str,
        file_type: str
    ) -> Generator[None, Any, Any]:
        """Вывод информации в текстовый файл"""
        job_uid = yield
        OUTPUT_FILES_DIR.mkdir(exist_ok=True)
        now = dt.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        file_name = f'{now_formatted}_{file_name}.{file_type}'
        file_path = OUTPUT_FILES_DIR / file_name
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text + '\n')
        record_status_log.overwrite_job_status(job_uid, 'END')
        logger.info(
            f'Задача {job_uid} - "{self.file_output.__doc__}" выполнена'
        )

    @coroutine
    def file_output_dependencies(self, text: str) -> Generator[None, Any, Any]:
        """Вывод информации о зависимостях в файл"""
        job_uid = yield # type: ignore
        file_path = URL_DEPENDENT
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text + '\n')
        record_status_log.overwrite_job_status(job_uid, 'END')
        logger.info(
            f'Задача {job_uid} - "{self.file_output.__doc__}" выполнена'
        )


working_file = WorkingFiles()

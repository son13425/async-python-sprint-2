import datetime as dt
import os.path
import time
from typing import Any, Generator, Optional
from pathlib import Path

from app.constants import (
    DATETIME_FORMAT,
    OUTPUT_FILES_DIR
)
from app.loggs.logger import logger
from app.utils.decorator import coroutine
from threading import Lock
from app.log_status.log_status import overwrite_job_status


lock = Lock()


class WorkingFiles():
    """Работа с файлами"""

    @coroutine
    def file_read(
        self,
        file_url: Path
    ) -> Optional[Generator[Optional[Any], None, None]]:
        """Чтeние файла"""
        job_uid = yield
        time.sleep(5)
        if os.path.exists(file_url):
            with open(file_url, encoding='utf-8') as file:
                text = file.readline()
                print(text)
                logger.info(
                    f'Задача {job_uid} - "{self.file_read.__doc__}" выполнена'
                )
            with lock:
                overwrite_job_status(job_uid, 'END')
        else:
            logger.error(
                f'Задача {job_uid} - "{self.file_read.__doc__}" '
                f'прервана: файл для запроса ({file_url}) не найден'
            )
            return None

    @coroutine
    def file_output(self, text: str, file_name: str, file_type: str) -> None:
        """Вывод информации в текстовый файл"""
        job_uid = yield
        OUTPUT_FILES_DIR.mkdir(exist_ok=True)
        now = dt.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        file_name = f'{now_formatted}_{file_name}.{file_type}'
        file_path = OUTPUT_FILES_DIR / file_name
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text + '\n')
        logger.info(
            f'Задача {job_uid} - "{self.file_output.__doc__}" выполнена'
        )
        with lock:
            overwrite_job_status(job_uid, 'END')


working_file = WorkingFiles()

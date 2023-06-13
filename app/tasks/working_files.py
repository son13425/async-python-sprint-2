import datetime as dt
from typing import Any, Generator, Optional
from pathlib import Path

from app.constants import (
    DATETIME_FORMAT,
    OUTPUT_FILES_DIR
)
from app.loggs.logger import logger, Notifies
from app.utils.decorator import coroutine


class WorkingFiles(metaclass=Notifies):
    """Работа с файлами"""

    def file_create(self, file_name: str, file_type: str) -> None:
        """Создание файла"""
        OUTPUT_FILES_DIR.mkdir(exist_ok=True)
        now = dt.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        file_name = f'{now_formatted}_{file_name}.{file_type}'
        file_path = OUTPUT_FILES_DIR / file_name
        file_path.touch(exist_ok=True)

    @coroutine
    def file_read(
        self,
        file_url: Path
    ) -> Generator[Optional[Any], None, None]:
        """Чтeние файла"""
        try:
            with open(file_url, encoding='utf-8') as file:
                text = file.readline()
                yield text
        except FileNotFoundError:
            logger.error(f'Файл данных запроса ({file_url}) не найден')
            return None

    def file_output(self, text: str, file_name: str, file_type: str) -> None:
        """Вывод информации в текстовый файл"""
        OUTPUT_FILES_DIR.mkdir(exist_ok=True)
        now = dt.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        file_name = f'{now_formatted}_{file_name}.{file_type}'
        file_path = OUTPUT_FILES_DIR / file_name
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text + '\n')


working_file = WorkingFiles()

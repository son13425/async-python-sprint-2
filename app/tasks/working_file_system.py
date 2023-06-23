from app.utils.decorator import coroutine
from app.loggs.logger import logger
from app.constants import BASE_DIR
from pathlib import Path
import time
import os
from app.constants import (
    OUTPUT_FILES_DIR
)
from threading import Lock
from app.log_status.log_status import overwrite_job_status


lock = Lock()


class WorkingFileSystem():
    """Работа с файловой системой"""

    @coroutine
    def dir_create(self, dir_name: str):
        """Создание директории"""
        job_uid = yield
        if not BASE_DIR.isdir(dir_name):
            BASE_DIR.mkdir(dir_name)
            logger.info(
                f'Задача {job_uid} - "{self.dir_create.__doc__} {dir_name}" '
                'выполнена'
            )
            with lock:
                overwrite_job_status(job_uid, 'END')
        else:
            logger.error(
                f'Задача {job_uid} - "{self.dir_create.__doc__} {dir_name}" '
                f'прервана: директория с именем {dir_name} уже существует'
            )

    @coroutine
    def dir_rename(self, dir_name: str, new_dir_name: str):
        """Переименование директории"""
        job_uid = yield
        time.sleep(5)
        if not BASE_DIR.isdir(new_dir_name):
            BASE_DIR.rename(dir_name, new_dir_name)
            logger.info(
                f'Задача {job_uid} - "{self.dir_rename.__doc__} {dir_name}" в'
                f' {new_dir_name} выполнена'
            )
            with lock:
                overwrite_job_status(job_uid, 'END')
        else:
            logger.error(
                f'Задача {job_uid} - "{self.dir_rename.__doc__} {dir_name}" '
                f'прервана: директория с именем {new_dir_name} уже существует'
            )

    @coroutine
    def dir_delete(self, dir_name: str):
        """Удаление директории"""
        job_uid = yield
        time.sleep(5)
        if BASE_DIR.isdir(dir_name):
            BASE_DIR.rmdir(dir_name)
            logger.info(
                f'Задача {job_uid} - "{self.dir_delete.__doc__} {dir_name}" '
                'выполнена'
            )
            with lock:
                overwrite_job_status(job_uid, 'END')
        else:
            logger.error(
                f'Задача {job_uid} - "{self.dir_delete.__doc__} {dir_name}" '
                f'прервана: директория с именем {dir_name} не найдена'
            )

    @coroutine
    def file_create(self, name: str, file_type: str) -> None:
        """Создание файла"""
        job_uid = yield
        time.sleep(20)
        OUTPUT_FILES_DIR.mkdir(exist_ok=True)
        file_name = f'{name}.{file_type}'
        file_path = OUTPUT_FILES_DIR / file_name
        file_path.touch(exist_ok=True)
        logger.info(
            f'Задача {job_uid} - "{self.file_create.__doc__} {file_name}" '
            'выполнена'
        )
        with lock:
            overwrite_job_status(job_uid, 'END')

    @coroutine
    def file_delete(self, file_url: Path) -> None:
        """Удаление файла"""
        job_uid = yield
        if os.path.exists(file_url):
            os.remove(file_url)
            logger.info(
                f'Задача {job_uid} - "{self.file_delete.__doc__} {file_url}" '
                'выполнена'
            )
            with lock:
                overwrite_job_status(job_uid, 'END')
        else:
            logger.error(
                f'Задача {job_uid} - "{self.file_delete.__doc__} {file_url}" '
                f'прервана: файл не найден'
            )


work_file_system = WorkingFileSystem()

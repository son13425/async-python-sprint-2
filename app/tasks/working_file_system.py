from app.utils.decorator import coroutine
from app.loggs.logger import logger
from app.constants import BASE_DIR
from pathlib import Path
import time
import os
from app.constants import (
    OUTPUT_FILES_DIR
)
from app.log_status.log_status import record_status_log


class WorkingFileSystem():
    """Работа с файловой системой"""

    @coroutine
    def dir_create(self, dir_name: str):
        """Создание директории"""
        job_uid = yield
        if os.path.exists(BASE_DIR / dir_name):
            record_status_log.overwrite_job_status(
                job_uid,
                'ABORTED'
            )
            logger.error(
                f'Задача {job_uid} - "{self.dir_create.__doc__} "{dir_name}" '
                f'прервана: директория с именем "{dir_name}" уже существует'
            )
        else:
            path = BASE_DIR / dir_name
            path.mkdir(exist_ok=True)
            record_status_log.overwrite_job_status(job_uid, 'END')
            logger.info(
                f'Задача {job_uid} - "{self.dir_create.__doc__} {dir_name}" '
                'выполнена'
            )
        return True

    @coroutine
    def dir_rename(self, dir_name: str, new_dir_name: str):
        """Переименование директории"""
        job_uid = yield
        time.sleep(5)
        if os.path.exists(BASE_DIR / new_dir_name):
            record_status_log.overwrite_job_status(
                job_uid,
                'ABORTED'
            )
            logger.error(
                f'Задача {job_uid} - "{self.dir_rename.__doc__} "{dir_name}" '
                f'прервана: директория с именем "{new_dir_name}" уже '
                'существует'
            )
        else:
            path = BASE_DIR / dir_name
            path_new = BASE_DIR / new_dir_name
            path.rename(path_new)
            record_status_log.overwrite_job_status(job_uid, 'END')
            logger.info(
                f'Задача {job_uid} - "{self.dir_rename.__doc__} "{dir_name}" '
                f'в "{new_dir_name}" выполнена'
            )

    @coroutine
    def dir_delete(self, dir_name: str):
        """Удаление директории"""
        job_uid = yield
        time.sleep(5)
        if os.path.exists(BASE_DIR / dir_name) is False:
            record_status_log.overwrite_job_status(
                job_uid,
                'ABORTED'
            )
            logger.error(
                f'Задача {job_uid} - "{self.dir_delete.__doc__} "{dir_name}" '
                f'прервана: директория с именем "{dir_name}" не найдена'
            )
        else:
            path = BASE_DIR / dir_name
            path.rmdir()
            record_status_log.overwrite_job_status(job_uid, 'END')
            logger.info(
                f'Задача {job_uid} - "{self.dir_delete.__doc__} "{dir_name}" '
                'выполнена'
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
        record_status_log.overwrite_job_status(job_uid, 'END')
        logger.info(
            f'Задача {job_uid} - "{self.file_create.__doc__} {file_name}" '
            'выполнена'
        )

    @coroutine
    def file_delete(self, file_url: Path) -> None:
        """Удаление файла"""
        job_uid = yield
        if os.path.exists(file_url):
            os.remove(file_url)
            record_status_log.overwrite_job_status(job_uid, 'END')
            logger.info(
                f'Задача {job_uid} - "{self.file_delete.__doc__} {file_url}" '
                'выполнена'
            )
        else:
            record_status_log.overwrite_job_status(
                job_uid,
                'ABORTED'
            )
            logger.error(
                f'Задача {job_uid} - "{self.file_delete.__doc__} {file_url}" '
                f'прервана: файл не найден'
            )


work_file_system = WorkingFileSystem()

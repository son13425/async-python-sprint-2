from app.job import Job
from app.tasks.working_files import working_file
from app.tasks.working_file_system import work_file_system
from app.tasks.working_network import working_network
from time import perf_counter
from app.constants import (
    DIR_NAME_FIRST,
    DIR_NAME_RENAME,
    FILE_FOR_READ,
    URL_FOR_PARSING,
    OUTPUT_FILES_DIR
)


job1 = Job(
    target=working_file.file_read,
    args=(FILE_FOR_READ, ),
    start_at=perf_counter() + 30
)
job2 = Job(
    target=work_file_system.file_create,
    args=('ddd', 'json'),
    max_working_time=5
)
job3 = Job(
    target=working_file.file_output,
    args=('Привет!', 'kkkk', 'json')
)
job4 = Job(
    target=work_file_system.dir_create,
    args=(DIR_NAME_FIRST, ),
)
job5 = Job(
    target=work_file_system.dir_rename,
    args=(DIR_NAME_FIRST, DIR_NAME_RENAME, ),
)
job6 = Job(
    target=work_file_system.dir_delete,
    args=(DIR_NAME_RENAME, ),
)
job7 = Job(
    target=working_network.get_request,
    args=(URL_FOR_PARSING, ),
)
job8 = Job(
    target=work_file_system.file_delete,
    args=(OUTPUT_FILES_DIR / 'ddd.json', ),
)


list_jobs = [job1, job2, job3, job4, job5, job6, job7, job8]

from app.job import Job
from app.tasks.working_files import working_file
from app.constants import FILE_FOR_READ
from time import perf_counter


job1 = Job(
    target=working_file.file_read,
    args=(FILE_FOR_READ, ),
    start_at=perf_counter() + 30
)
job2 = Job(
    target=working_file.file_create,
    args=('ddd', 'json'),
    max_working_time=5
)
job3 = Job(
    target=working_file.file_output,
    args=('Привет!', 'kkkk', 'json')
)

list_jobs = [job1, job2, job3]

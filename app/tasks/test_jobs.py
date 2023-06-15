from app.job import Job
from app.tasks.working_files import working_file
from app.constants import FILE_FOR_READ

job1 = Job(
    target=working_file.file_read,
    args=(FILE_FOR_READ, )
)
job2 = Job(
    target=working_file.file_create,
    args=('ddd', 'json')
)
job3 = Job(
    target=working_file.file_output,
    args=('Привет!', 'kkkk', 'json')
)

list_jobs = [job1, job2, job3]

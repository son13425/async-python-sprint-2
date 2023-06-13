from app.tasks.working_files import working_file
from app.constants import FILE_FOR_READ
from app.job import Job
from app.scheduler import Scheduler


job1 = Job(working_file.file_read, args=(FILE_FOR_READ, ))
loop = Scheduler()
loop.schedule(job1)
loop.run()


# file_output('ghbdtn', 'aaa', 'txt')
# file_create('bbb', 'txt')

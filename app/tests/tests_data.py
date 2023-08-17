from pathlib import Path

from app.job import Job
from app.tasks.working_file_system import work_file_system

FILE_EXAMPLE = Path(__file__).parent / 'tests' / 'file_example.json'

file_example_content = [
    {
        "job_uid": "5121f22cdf6f4a6ca7c00f465badefe9",
        "info_job": {
            "target": "file_create",
            "args": "('ddd', 'json')",
            "kwargs": "{}",
            "start_at": "None",
            "max_working_time": 2,
            "tries": 0,
            "dependencies": "[]"
        },
        "info_status": {
            "status": "IN_PROGRESS",
            "current_tries": 1
        }
    }
]

job_example = Job(
    target=work_file_system.file_create,
    args=('example', 'json'),
    max_working_time=2
)

data = {
    "target": "file_create",
    "args": "('ddd', 'json')",
    "kwargs": "{}",
    "start_at": "None",
    "max_working_time": 2,
    "tries": 0,
    "dependencies": "[]"
}

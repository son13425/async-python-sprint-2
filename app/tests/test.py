import unittest

from app.log_status.log_status import record_status_log
from app.tests.tests_data import (FILE_EXAMPLE, data, data_error,
                                  file_example_content, job_example)

FILE_STATUS_LOG = FILE_EXAMPLE


class MyTest(unittest.TestCase):
    """Тесты кода приложения"""

    @classmethod
    def setUpClass(cls) -> None:
        print('Тесты запущены')

    @classmethod
    def tearDownClass(cls) -> None:
        print('Тесты успешно пройдены')

    def setUp(self) -> None:
        print('Тестирую...')

    def tearDown(self) -> None:
        print('Успешно!')

    def test_func_converting_job_to_dict(self):
        self.assertEqual(
            record_status_log.converting_job_to_dict(job_example),
            data
        )

    def test_with_error_converting_job_to_dict(self):
        self.assertEqual(
            record_status_log.converting_job_to_dict(job_example),
            data_error,
            msg='Данные не соответствуют ожиданию'
        )

    def test_func_read_status_log(self):
        self.assertEqual(
            record_status_log.read_status_log(FILE_EXAMPLE),
            file_example_content
        )

    def test_with_error_read_status_log(self):
        self.assertEqual(
            record_status_log.read_status_log(FILE_EXAMPLE),
            data_error,
            msg='Данные не соответствуют ожиданию'
        )


if __name__ == '__main__':
    unittest.main()

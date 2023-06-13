from pathlib import Path


# количество одновременно обрабатываемых задач
MAX_WORKERS = 10

# формат даты
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'


# работа с файлами

# базовая директория
BASE_DIR = Path(__file__).parent
# директория для работы с файлами
WORKING_FILES_DIR = BASE_DIR / 'external'
# директория для вывода файлов
OUTPUT_FILES_DIR = WORKING_FILES_DIR / 'outputs'
# файл для чтения
NAME_FILE_FOR_READ = 'example_text_file.txt'
FILE_FOR_READ = WORKING_FILES_DIR / NAME_FILE_FOR_READ
# имя файл для вывода
NAME_FILE_FOR_OUTPUT = 'output_file'


# формат сообщений логгера
FORMAT_LOGGER = (
    '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
)
# адрес файла вывода логов
FILE_LOGGER = BASE_DIR / 'loggs' / 'application-log.log'

#  Планировщик для выполнения поступающих задач

## Краткое описание проекта

Базовые функции:
- Планировщик одновременно может выполнять до 10 задач (дефолтное значение, может быть изменено в файле app/constants.py).
- Возможность добавить задачу в планировщик и запустить её в рамках ограничений планировщика и настроек (добавьте задачу в список list_jobs в файле app/tasks/test_jobs.py).
- При штатном завершении работы планировщик сохраняет статус выполняемых и ожидающих задач в файле app/log_status/log_status.json.
- После рестарта восстанавливается последнее состояние и задачи продолжают выполняться.

Реализованные опции задач:
- У задачи может быть указана длительность выполнения (опциональный параметр). Если параметр указан, то задача прекращает выполняться, если время выполнения превысило указанный параметр.
- У задачи может быть указано время запуска (опциональный параметр). Если параметр указан, то задача стартует в указанный временной период.
- У задачи может быть указан параметр количества рестартов (опциональный параметр). Если в ходе выполнения задачи произошёл сбой или задачи-зависимости не были выполнены, то задача будет перезапущена указанное количество раз. Если параметр не указан, то количество рестартов равно 0.
- У задачи может быть указаны зависимости — задача или задачи, от которых зависит её выполнение (опциональный параметр). Если параметр указан, то задача не может стартовать до момента, пока не будут завершены задачи-зависимости.

Типы выполняемых задач:
- работа с файловой системой: создание, удаление, изменение директорий и файлов;
- работа с файлами: создание, чтение, запись;
- работа с сетью: обработка ссылок (GET-запросы) и анализ полученного результата;
- конвеер выполнения основной задачи минимум из 3 задач, зависящих друг от друга и выполняющихся последовательно друг за другом.


### Технологии

- Python 3.10
- multiprocessing
- concurrent.futures
- корутины и генераторы

### Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone
```

```
cd async-python-sprint-2
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запустить приложение:

```
python3 main.py
```

Тестировать приложение:

```
python3 -m external.tests.test
```

### Автор.
[Оксана Широкова](https://github.com/son13425)


## Лицензия
Проект выпущен под лицензией [MIT](https://github.com/son13425/async-python-sprint-2/blob/main/COPYING.txt)

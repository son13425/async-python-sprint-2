from ..external import FILE_FOR_READ


def file_read():
    try:
        with open(FILE_FOR_READ, encoding='utf-8') as file:
            text = file.readline()
            return text
    except FileNotFoundError:
        print(f'Файл данных запроса ({FILE_FOR_READ}) не найден')


print(file_read())

# def file_output(results):
#     """Выводит результат в файл csv"""
#     results_dir = BASE_DIR / 'results'
#     results_dir.mkdir(exist_ok=True)
#     now = datetime.datetime.now()
#     now_formatted = now.strftime(DT_FORMAT)
#     file_name = f'Results_{now_formatted}.csv'
#     file_path = results_dir / file_name
#     with open(file_path, 'w', encoding='utf-8') as file:
#         writer = csv.writer(
#             file, dialect='unix',
#             delimiter=';',
#             quoting=csv.QUOTE_NONE
#         )
#         writer.writerows(results)
#     logging.info(f'Файл с результатами был сохранён: {file_path}')

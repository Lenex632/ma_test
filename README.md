## Парсер для сайта Метро

Делалось как тестовое. Небольшой парсер по категориям для сайта METRO.

Нашёл API METRO. Он использует GraphQL. Так как строгих ограничений в задании не было, решил написать простой
запрос, который будет искать все необходимые данные, а после записывать в CSV-файл results.csv.

В репозитории присутствуют файл со скриптом parser.py, стандартный .gitignore, файл с зависимостями requirements.txt и 
пример с результатом скрипта results_example.csv.

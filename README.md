# this-has-answers
service for calculating

- Сервис принимает математическое выражение с переменными и значения самих переменных.
- Возвращает значение выражения.
- Информативно обрабатывает возможные исключения.
- Api вынесено в отдельное приложение.
- Доступно всем, токены не требуются.
- Реализовано через api_view функцию.
- Написано несколько базовых тестов.

### Как запустить проект:
Склонировать репозиторий:
```
https://github.com/FFFSanchez/this-has-answers.git
```

Создать свой .env в корне проекта в формате (SECRET_KEY можно сгенерить тут https://djecrety.ir/):
```
SECRET_KEY=***
```

* Запуск через виртуальное окружение:

```
python -m venv env
source venv/Scripts/activate
pip install -r requirements.txt

- Запуск тестов:
python manage.py test

python manage.py runserver
```

* Запуск через Docker:

```
docker build -t opencode .
docker run --name opencode_container --env-file .env --rm -p 8000:8000 opencode
```

По адресу http://127.0.0.1:8000/api/compute/ будут доступны GET и POST запросы

## Примеры использования:
```
GET запрос
{
    "expression": "Напишите выражение, например: lg(5*a+2*b)",
    "varies": "Напишите переменные в формате словаря"
}
```

```
POST запрос
{
    "expression": "a+2*b",
    "varies": {
            "a": 2.5,
            "b": 1
        }
}
ответ:
{
    "result": 4.5
}
```
Либо в ответе будет информативное сообщение об ошибке. Ошибки обрабатываются все.


### Автор: 
Александр Трифонов

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

Создать свой .env в корне проекта в формате (SECRET_KEY можно сгенерить тут https://djecrety.ir/):
```
SECRET_KEY=***
```

1) Запуск через виртуальное окружение:

```
python -m venv env
source venv/Scripts/activate
pip install -r requirements.txt
python manage.py runserver
```

2) Запуск через Docker:

```
docker build -t opencode .
docker run --name opencode_container --env-file .env --rm -p 8000:8000 opencode
```

По адресу http://127.0.0.1:8000/api/compute/ будут доступны GET и POST запросы
- Тесты запускаются так:
```
python manage.py test
```
- Формат взаимодействия такой (я использовал POSTMAN):
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
Либо информативное сообщение об ошибке. Ошибки обрабатываются все.


### Автор: 
Александр Трифонов

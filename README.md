# this-has-answers
service for calculating

### Как запустить проект:

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

По адресу http://127.0.0.1:8000/api/v1/compute/ будут доступны GET и POST запросы
Формат взаимодействия такой:
```
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
Либо сообщение об ошибке, в зависимости от того, что неправильно передали в запросе.

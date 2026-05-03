# Сайт о достопримечательносьтях Москвы 

Этот сайт отображает на карте некаторые достопримечательности Москвы и может принимать новые места.

## Как установить

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

## Как Запустить проекта

запкстите миграцыи:
```
python manage.py migrate
```
После этого запустите сервер:
```
python manage.py runserver
```

## Настройки

.env файл:
```
DEBUG=Режим отладки(True/False)
ALLOWED_HOSTS=список строк, представляющих хост.сервер, который обслуживается этим проектом
SECRET_KEY=Секретный ключ проекта установки джанго
```

## Источники данных

Программа берет информацию из json-файлов, распологающегося по адресу "/static/places"
```
{
    "title": "Экскурсионный проект «Крыши24.рф»",
    "imgs": [
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/af7b8599fec9d2542a011f1d01d459e2.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/965c5a3ff5b2431e646d30b6744afd2d.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/06868b2b01ff8db506cd21956a6cb636.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/a8cc3e03f56413275ded99e51226a70f.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/44e96733303e7490aaa1cf2eebfbbfff.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/fadf618505b087fa539e883f33f850b2.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/ec461a89a1d0d5a4cb7c81f1fc0a4e89.jpg"
    ],
    "description_short": "Хотите увидеть Москву с высоты и разделить яркие впечатления с друзьями? В этом поможет проект «Крыши24.рф». Вы можете выбрать крышу из множества интересных вариантов и провести там свидание, вечеринку, творческое занятие, фотосессию или что-то ещё.",
    "description_long": "<p>Проект «Крыши24.рф» проводит экскурсии и мероприятия на крышах, откуда открываются впечатляющие виды на мегаполис. </p><h4>Экскурсии на высоте</h4><p>Список крыш, на которые можно подняться, очень велик, и находятся...
    "coordinates": {
        "lng": "37.32478399999957",
        "lat": "55.70731600000015"
    }
}

```

## load_place.py

Для того, чтобы загрузить данные про новые места, можно использовать функуию load_place.py. Способ применения:
```
python manage.py load_place [url]
```


## Цель проекта

Код написан в образовательных целях... 
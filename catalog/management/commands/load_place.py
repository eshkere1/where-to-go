import json
import sys
from os import makedirs
from os.path import join
from pathlib import Path

import requests
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from requests.exceptions import RequestException

from catalog.models import Place, Image

class Command(BaseCommand):
    help = "Загружает файлы json и данные из них в базу данных"
    saved_path = "static/places"

    def add_arguments(self, parser):
        parser.add_argument(
            "--url", type=str, help="URL к JSON файлу", default=None
        )

    def download_github_json(
        self,
        owner="devmanorg",
        repo="where-to-go-places",
        download_dirs="places",
    ):
        github_url = join(
            f"https://api.github.com/repos/{owner}/{repo}/contents/",
            download_dirs,
        )
        try:
            response = requests.get(github_url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 401:
                sys.stderr.write(
                    "Ошибка 401: Не авторизован. Пробуем перелогиниться...\n"
                )
            elif status_code == 404:
                sys.stderr.write("Ошибка 404: Ресурс не найден.\n")
            elif status_code == 500:
                sys.stderr.write(
                    "Ошибка 500: Внутренняя ошибка сервера. Повторяем запрос позже...\n"
                )
            else:
                sys.stderr.write(f"HTTP ошибка {status_code}: {e}\n")
            return  # Важно: выходим при ошибке
        except requests.exceptions.Timeout:
            sys.stderr.write("Таймаут: Сервер не отвечает\n")
            return
        except requests.exceptions.ConnectionError:
            sys.stderr.write("Ошибка соединения: Сервер недоступен\n")
            return
        except RequestException as e:
            sys.stderr.write(f"Общая ошибка запроса: {e}\n")
            return

        files = response.json()
        for file_info in files:
            if file_info["name"].endswith(".json"):
                file_response = requests.get(file_info["download_url"])
                file_response.raise_for_status()
                file_data = file_response.json()
                makedirs(self.saved_path, exist_ok=True)
                with open(
                    join(self.saved_path, file_info["name"]),
                    "w",
                    encoding="utf-8",
                ) as file:
                    json.dump(file_data, file, ensure_ascii=False)

    def process_place_data(self, place_data):
        """Обработка данных одного места"""
        place_obj, created = Place.objects.get_or_create(
            title=place_data["title"],
            short_description=place_data["description_short"],
            long_description=place_data["description_long"],
            longitude=float(place_data["coordinates"]["lng"]),
            latitude=float(place_data["coordinates"]["lat"]),
        )

        Image.objects.filter(place=place_obj).delete()

        for number, img_url in enumerate(place_data["imgs"], 1):
            try:
                response = requests.get(img_url, timeout=10)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Ошибка загрузки {img_url}: {e}"
                    )
                )
                continue

            img_name = f"place_{place_obj.id}_{number}.jpg"

            try:
                Image.objects.create(
                    place=place_obj,
                    index=number,
                    image=ContentFile(
                        response.content, name=img_name
                    ),
                )
            except (IntegrityError, ValidationError) as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Ошибка сохранения изображения {img_name}: {e}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Загружена картинка {img_name}"
                    )
                )

    def handle(self, *args, **options):
        url = options.get("url")
        
        if url:
            # Загружаем только одно место по URL
            self.stdout.write(f"Загрузка места по URL: {url}")
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                place_data = response.json()
                self.process_place_data(place_data)
                self.stdout.write(
                    self.style.SUCCESS(f"Место успешно загружено из {url}")
                )
            except requests.exceptions.RequestException as e:
                self.stdout.write(
                    self.style.ERROR(f"Ошибка загрузки из {url}: {e}")
                )
        else:
            # Загружаем все места из репозитория
            self.stdout.write("Загрузка всех мест из репозитория...")
            self.download_github_json()
            
            # Обрабатываем все загруженные файлы
            for file_path in Path("static/places").iterdir():
                if file_path.is_file() and file_path.suffix == ".json":
                    with open(file_path, "r", encoding="utf-8") as file:
                        place_data = json.load(file)
                        self.process_place_data(place_data)
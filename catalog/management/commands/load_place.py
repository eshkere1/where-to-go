import requests
import sys
import json
from requests.exceptions import HTTPError, RequestException
from os import makedirs
from os.path import join
from django.core.management.base import BaseCommand
from catalog.models import Place, Image
from pathlib import Path
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = "Загружает файлы json и данные из них в базу данных"
    saved_path = 'static/places'
    def add_arguments(self, parser):
        parser.add_argument('--url', type=str, help='URL к JSON файлу', default=None)
    def download_github_json(self, owner='devmanorg', repo='where-to-go-places', download_dirs='places'):
        github_url = join(f'https://api.github.com/repos/{owner}/{repo}/contents/', download_dirs)
        try:
            response = requests.get(github_url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_codeя
            if status_code == 401:
                sys.stderr.write("Ошибка 401: Не авторизован. Пробуем перелогиниться...\n")
            elif status_code == 404:
                sys.stderr.write("Ошибка 404: Ресурс не найден.\n")
            elif status_code == 500:
                sys.stderr.write("Ошибка 500: Внутренняя ошибка сервера. Повторяем запрос позже...\n")
            else:
                sys.stderr.write(f"HTTP ошибка {status_code}: {e}\n")
        except requests.exceptions.Timeout:
            sys.stderr.write("Таймаут: Сервер не отвечает\n")
        except requests.exceptions.ConnectionError:
            sys.stderr.write("Ошибка соединения: Сервер недоступен\n")
        except RequestException as e:
            sys.stderr.write(f"Общая ошибка запроса: {e}\n")
            
        files = response.json()
        for file_info in files:
            if file_info['name'].endswith('.json'):
                file_response = requests.get(file_info['download_url'])
                file_response.raise_for_status()
                file_data = file_response.json()
                makedirs(self.saved_path, exist_ok=True)
                with open(join(self.saved_path, file_info['name']), 'w', encoding='utf-8') as file:
                    json.dump(file_data, file, ensure_ascii=False)
    

    def handle(self, *args, **options):
        url = options.get("url")
        if url:
            self.stdout.write()
        else:
            self.download_github_json()

        for file_path in Path('static/places').iterdir():
            if file_path.is_file():
                with open(file_path, 'r', encoding='utf-8') as file:
                    place = json.load(file)
                    place_obj, create = Place.objects.get_or_create(
                        title=place['title'],
                        short_description=place['description_short'],
                        long_description=place['description_long'],
                        longitude=float(place['coordinates']['lng']),
                        latitude=float(place['coordinates']['lat']),
                    )
                    
                    Image.objects.filter(place=place_obj).delete()
                    
                    for number, img_url in enumerate(place['imgs'], 1):
                        try:
                            response = requests.get(img_url)
                            response.raise_for_status()
                            img_name = img_url.split('/')[-1]
                            if '?' in img_name:
                                img_name = img_name.split('?')[0]
                            if not img_name or '.' not in img_name:
                                img_name = f'image_{number}.jpg'
                            Image.objects.create(
                                place=place_obj,
                                images_index=number,
                                image=ContentFile(response.content, name=img_name),
                            )
                            self.stdout.write(self.style.SUCCESS(f'Загружена картинка {img_name}'))

                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f' Ошибка загрузки {img_url}: {e}'))
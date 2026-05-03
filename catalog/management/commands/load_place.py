import requests
from os import makedirs
from os.path import join
import json
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
        response = requests.get(github_url)
        response.raise_for_status()
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
                    data = json.load(file)
                    place_obj, create = Place.objects.get_or_create(
                        title=data['title'],
                        description_short=data['description_short'],
                        description_long=data['description_long'],
                        longitude=float(data['coordinates']['lng']),
                        latitude=float(data['coordinates']['lat']),
                    )
                    
                    Image.objects.filter(place=place_obj).delete()
                    
                    for number, img_url in enumerate(data['imgs'], 1):
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
                                images_order=number,
                                image=ContentFile(response.content, name=img_name),
                            )
                            self.stdout.write(self.style.SUCCESS(f'Загружена картинка {img_name}'))
                            
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f' Ошибка загрузки {img_url}: {e}'))

# def get_json_info_by_file(path):
#     with codecs.open(path, 'r', 'utf_8_sig') as file:
#         data = file.read()
#     parsed_place = json.loads(date)
#     return parsed_place

# def get_json_info_by_url(url):
#     response = requests.get(url)
#     response.raise_for_status()
#     return response.json()

# def parse_place_with_images(url):
#     place = get_json_info_by_url(url)
#     parsed_place = Place.objects.get_or_creat(
#         title=place['title'],
#         defaults={
#             'description_short':place['description_short'],
#             'description_short':place['description_short'],
#             'longitude':Decimal(place['coordinates']['lng']),
#             'latitude':Decimal(place['coordinates']['lat']),
#         }
#     )[0]
#     for img_number, img_url in enumerate(place['imgs']):
#         try:
#             response = requests
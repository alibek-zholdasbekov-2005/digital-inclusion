import json
import os
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon
from directories.models import District

class Command(BaseCommand):
    help = 'Импорт границ районов Алматы из GeoJSON'

    def handle(self, *args, **options):
        file_path = 'almaty-districts.geo.json'
        
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f'Файл {file_path} не найден!'))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for feature in data['features']:
            name_ru = feature['properties'].get('nameRu')
            geom_data = feature['geometry']

            geojson_str = json.dumps(geom_data)
            geometry = GEOSGeometry(geojson_str)

            if isinstance(geometry, Polygon):
                geometry = MultiPolygon(geometry)

            district, created = District.objects.update_or_create(
                name_ru=name_ru,
                defaults={
                    'geometry': geometry,
                    'is_deleted': False
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Создан район: {name_ru}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Обновлены границы района: {name_ru}'))

        self.stdout.write(self.style.SUCCESS('Импорт успешно завершен!'))
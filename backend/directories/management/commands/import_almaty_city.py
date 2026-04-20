import json
import os
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon
from directories.models import District

class Command(BaseCommand):
    help = 'Импорт общих границ города Алматы из GeoJSON'

    def handle(self, *args, **options):
        file_path = 'almaty.geo.json'
        
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f'Файл {file_path} не найден!'))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        feature = data['features'][0]
        name_ru = feature['properties'].get('nameRu', 'г. Алматы')
        geom_data = feature['geometry']

        geojson_str = json.dumps(geom_data)
        geometry = GEOSGeometry(geojson_str)

        if isinstance(geometry, Polygon):
            geometry = MultiPolygon(geometry)

        district, created = District.objects.update_or_create(
            name_ru="г. Алматы",
            defaults={
                'geometry': geometry,
                'is_deleted': False
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Создана запись для г. Алматы с границами.'))
        else:
            self.stdout.write(self.style.SUCCESS('Границы для г. Алматы обновлены.'))

        self.stdout.write(self.style.SUCCESS('Импорт города завершен!'))
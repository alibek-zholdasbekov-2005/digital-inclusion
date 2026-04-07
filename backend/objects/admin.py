from django.conf import settings
from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import *

YANDEX_JS_URL = f'https://api-maps.yandex.ru/2.1/?lang=ru_RU&apikey={settings.YANDEX_MAPS_API_KEY}'

class PhotoInline(admin.TabularInline): model = ObjectPhoto; extra = 1
class SubObjectInline(admin.TabularInline): model = SubObject; extra = 0
class TerritoryInline(admin.StackedInline): model = ObjectTerritory; extra = 1
class EntranceInline(admin.StackedInline): model = EntranceGroup; extra = 1

@admin.register(AccessibilityObject)
class AccessibilityObjectAdmin(LeafletGeoAdmin):
    fieldsets = (
        ('Статусы', {'fields': ('sending_status', 'report_photo', 'object_status')}),
        ('Инфо', {'fields': ('name_ru', 'full_legal_name', 'district', 'street', 'house_number')}),
        ('Карта', {'fields': ('location', 'polygon')}),
        ('Тип', {'fields': ('category', 'activity_type', 'ownership_type', 'responsible_body')}),
    )
    inlines = [SubObjectInline, TerritoryInline, EntranceInline, PhotoInline]
    class Media:
        js = (
            YANDEX_JS_URL,
            'https://cdn.jsdelivr.net/gh/shramov/leaflet-plugins@master/layer/tile/Yandex.js',
            'js/yandex_map.js',
        )

class StopAccInline(admin.StackedInline): model = StopAccessibility; extra = 1
class StopPlatInline(admin.StackedInline): model = StopPlatform; extra = 1
class StopPavInline(admin.StackedInline): model = StopPavilion; extra = 1

@admin.register(BusStop)
class BusStopAdmin(LeafletGeoAdmin):
    list_display = ('stop_name', 'district')
    inlines = [StopAccInline, StopPlatInline, StopPavInline]
    class Media:
        js = (
            YANDEX_JS_URL,
            'https://cdn.jsdelivr.net/gh/shramov/leaflet-plugins@master/layer/tile/Yandex.js',
            'js/yandex_map.js',
        )
from django.conf import settings
from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import (
    District, Category, ActivityType, 
    AccessibilityCategory, OwnershipEntity, 
    ResponsibleBody, StreetCategory, PassportStatus
)
YANDEX_JS_URL = f'https://api-maps.yandex.ru/2.1/?lang=ru_RU&apikey={settings.YANDEX_MAPS_API_KEY}'
@admin.register(District)
class DistrictAdmin(LeafletGeoAdmin):
    list_display = ('id', 'name_ru', 'name_kz', 'akim_name', 'is_deleted')
    list_editable = ('is_deleted',)
    search_fields = ('name_ru', 'name_kz')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name_ru', 'name_kz')
        }),
        ('Дополнительно', {
            'fields': ('gerb', 'akim_name', 'is_deleted')
        }),
        ('Карта границ района', {
            'fields': ('geometry',),
        }),
    )
    class Media:
        js = (
            YANDEX_JS_URL,
            'https://cdn.jsdelivr.net/gh/shramov/leaflet-plugins@master/layer/tile/Yandex.js',
            'js/yandex_map.js',
        )
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('sort_order', 'display_icon', 'name_ru', 'name_kz', 'color')
    
    list_editable = ('sort_order', 'color')
    
    list_display_links = ('name_ru',) 
    
    search_fields = ('name_ru', 'name_kz')

    def display_icon(self, obj):
        if obj.icon:
            return mark_safe(f'<img src="{obj.icon.url}" width="30" height="30" style="object-fit:contain" />')
        return "—"
    display_icon.short_description = "Иконка"
@admin.register(AccessibilityCategory)
class AccessibilityCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name_ru', 'name_kz')
    search_fields = ('code', 'name_ru')

@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_ru', 'name_kz')
    search_fields = ('name_ru', 'name_kz')

@admin.register(OwnershipEntity)
class OwnershipEntityAdmin(admin.ModelAdmin): pass

@admin.register(ResponsibleBody)
class ResponsibleBodyAdmin(admin.ModelAdmin): pass

@admin.register(StreetCategory)
class StreetCategoryAdmin(admin.ModelAdmin): pass

@admin.register(PassportStatus)
class PassportStatusAdmin(admin.ModelAdmin): pass

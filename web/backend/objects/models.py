from django.conf import settings
from django.contrib.gis.db import models as gis_models
from django.db import models
from simple_history.models import HistoricalRecords
from directories.models import (
    District, Category, ActivityType, OwnershipEntity,
    ResponsibleBody, PassportStatus, Street, StreetCategory
)

class AccessibilityObject(gis_models.Model):
    """Основная модель паспорта здания"""
    MODERATION_DRAFT = 'draft'
    MODERATION_PENDING = 'pending'
    MODERATION_APPROVED = 'approved'
    MODERATION_REJECTED = 'rejected'
    MODERATION_CHOICES = [
        (MODERATION_DRAFT, 'Черновик'),
        (MODERATION_PENDING, 'На модерации'),
        (MODERATION_APPROVED, 'Одобрено'),
        (MODERATION_REJECTED, 'Отклонено'),
    ]

    sending_status = models.ForeignKey(PassportStatus, on_delete=models.SET_NULL, null=True, blank=True)
    moderation_state = models.CharField(
        "Статус модерации", max_length=16,
        choices=MODERATION_CHOICES, default=MODERATION_DRAFT,
    )
    rejection_reason = models.TextField("Причина отклонения", blank=True, default='')

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='submitted_objects',
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    name_ru = models.CharField("Название (RU)", max_length=500, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)
    full_legal_name = models.TextField("Юридическое название", blank=True, null=True)

    location = gis_models.PointField("Точка (Point)", srid=4326, null=True, blank=True)
    polygon = gis_models.MultiPolygonField("Контур (Polygon)", srid=4326, blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.PROTECT, null=True, blank=True)
    ownership_type = models.ForeignKey(OwnershipEntity, on_delete=models.PROTECT, null=True, blank=True)
    responsible_body = models.ForeignKey(ResponsibleBody, on_delete=models.PROTECT, null=True, blank=True)

    history = HistoricalRecords()

    @property
    def accessibility_summary(self):

        results = self.results.all()
        if not results:
            return "Нет данных"
        
        return "Данные обрабатываются"

    class Meta:
        verbose_name = "Паспорт объекта"
        verbose_name_plural = "1. Паспорта объектов"

    def __str__(self): 
        return str(self.name_ru) if self.name_ru else "Объект без названия"


class ObjectTerritory(models.Model):
    object = models.OneToOneField(AccessibilityObject, on_delete=models.CASCADE, related_name='territory')
    entrance_width_ok = models.BooleanField("Ширина прохода > 90см", default=False)
    parking_has_disabled_spots = models.BooleanField("Парковка для МГН", default=False)

class EntranceGroup(models.Model):
    object = models.OneToOneField(AccessibilityObject, on_delete=models.CASCADE, related_name='entrance_group')
    has_ramp = models.BooleanField("Наличие пандуса", default=False)
    has_braille = models.BooleanField("Наличие Брайля", default=False)
    has_call_button = models.BooleanField("Кнопка вызова", default=False)
    has_visual_info = models.BooleanField("Визуальная информация", default=False)

class MovementWays(models.Model):
    object = models.OneToOneField(AccessibilityObject, on_delete=models.CASCADE, related_name='movement_ways')
    width_ok = models.BooleanField("Ширина путей в норме", default=False)
    has_handrails = models.BooleanField("Наличие поручней", default=False)
    tactile_indicators = models.BooleanField("Тактильные указатели", default=False)

class ServiceZones(models.Model):
    object = models.OneToOneField(AccessibilityObject, on_delete=models.CASCADE, related_name='service_zones')
    counter_height_ok = models.BooleanField("Высота стоек в норме", default=False)

class SanitaryRooms(models.Model):
    object = models.OneToOneField(AccessibilityObject, on_delete=models.CASCADE, related_name='sanitary_rooms')
    toilet_accessible = models.BooleanField("Спец. туалет доступен", default=False)

class InfoTelecom(models.Model):
    object = models.OneToOneField(AccessibilityObject, on_delete=models.CASCADE, related_name='info_telecom')
    has_audio_guide = models.BooleanField("Аудиогид", default=False)
    induction_loop = models.BooleanField("Индукционная петля", default=False)
    has_visual_info = models.BooleanField("Электронное табло", default=False)

class ObjectPhoto(models.Model):
    object = models.ForeignKey(AccessibilityObject, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField("Фото", upload_to='objects/')

class SubObject(models.Model):
    parent_object = models.ForeignKey(AccessibilityObject, on_delete=models.CASCADE, related_name='sub_objects')
    name = models.CharField("Наименование", max_length=255)

class ObjectAccessibilityResult(models.Model):
    """Таблица итогов (К, О, З, С) — заполняется автоматически через signals.py"""
    object = models.ForeignKey(AccessibilityObject, on_delete=models.CASCADE, related_name='results')
    section = models.CharField("Раздел", max_length=50)
    k_status = models.CharField("К", max_length=20, default='not_accessible')
    o_status = models.CharField("О", max_length=20, default='not_accessible')
    z_status = models.CharField("З", max_length=20, default='not_accessible')
    s_status = models.CharField("С", max_length=20, default='not_accessible')
    
    class Meta:
        verbose_name = "Заключение по разделу"
        verbose_name_plural = "3. Заключения о доступности"
        unique_together = ('object', 'section')

class BusStop(gis_models.Model):
    sending_status = models.ForeignKey(PassportStatus, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Статус отправки", related_name="stop_status")
    rejection_reason = models.TextField("Причина отклонения", blank=True, null=True)
    report_photo = models.ImageField("Фото отчет", upload_to='stops/reports/', blank=True, null=True)

    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Район")
    stop_name = models.CharField("Остановка", max_length=255, null=True, blank=True)
    comment = models.TextField("Комментарии", blank=True, null=True)
    not_in_tx = models.BooleanField("Нет в ТХ", default=False)

    location = gis_models.PointField("Координаты", srid=4326, null=True, blank=True)
    
    ownership_type = models.ForeignKey(OwnershipEntity, on_delete=models.PROTECT, null=True, blank=True)
    responsible_body = models.ForeignKey(ResponsibleBody, on_delete=models.PROTECT, null=True, blank=True)

    @property
    def total_status(self):
        try:
            p = self.platform
            return "Доступна" if p.has_tactile_tile else "Частично доступна"
        except:
            return "Анкета не заполнена"

    class Meta:
        verbose_name = "Паспорт остановки"
        verbose_name_plural = "2. Паспорта остановок"

    def __str__(self): 
        return str(self.stop_name) if self.stop_name else "Остановка без названия"

class StopAccessibility(models.Model):
    stop = models.OneToOneField(BusStop, on_delete=models.CASCADE, related_name='accessibility')
    street_cat = models.ForeignKey(StreetCategory, on_delete=models.SET_NULL, null=True, blank=True)
    has_dedicated_lane = models.BooleanField("Выделенная полоса", default=False)

class StopPlatform(models.Model):
    stop = models.OneToOneField(BusStop, on_delete=models.CASCADE, related_name='platform')
    is_level_with_bus = models.BooleanField("В один уровень с краем дороги", default=False)
    has_tactile_tile = models.BooleanField("Тактильная плитка", default=False)

class StopPavilion(models.Model):
    stop = models.OneToOneField(BusStop, on_delete=models.CASCADE, related_name='pavilion')
    has_lighting = models.BooleanField("Освещение", default=False)
    has_benches = models.BooleanField("Скамейки", default=False)
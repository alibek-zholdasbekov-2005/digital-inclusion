from django.contrib.gis.db import models as gis_models
from django.db import models
from simple_history.models import HistoricalRecords
from directories.models import (
    District, Category, ActivityType, OwnershipEntity, 
    ResponsibleBody, PassportStatus, Street, StreetCategory
)

class AccessibilityObject(gis_models.Model):
    sending_status = models.ForeignKey(PassportStatus, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Статус отправки")
    rejection_reason = models.TextField("Причина отклонения", blank=True, null=True)
    report_photo = models.ImageField("Фото отчет", upload_to='reports/', blank=True, null=True)
    object_status = models.CharField("Статус объекта", max_length=100, blank=True, null=True)

    name_ru = models.CharField("Наименование на русском", max_length=500, null=True, blank=True)
    full_legal_name = models.TextField("Полное юридическое наименование", blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.PROTECT, verbose_name="Район", null=True, blank=True)
    street = models.ForeignKey(Street, on_delete=models.SET_NULL, null=True, blank=True)
    house_number = models.CharField("Номер дома", max_length=20, blank=True, null=True)
    
    location = gis_models.PointField("Точка координат", srid=4326, null=True, blank=True)
    polygon = gis_models.MultiPolygonField("Полигоны координат", srid=4326, blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.PROTECT, null=True, blank=True)
    ownership_type = models.ForeignKey(OwnershipEntity, on_delete=models.PROTECT, null=True, blank=True)
    responsible_body = models.ForeignKey(ResponsibleBody, on_delete=models.PROTECT, null=True, blank=True)

    history = HistoricalRecords()

    @property
    def accessibility_calculation(self):
        return {"status": "Расчет активен"}

    class Meta:
        verbose_name = "Паспорт объекта"
        verbose_name_plural = "1. Паспорта объектов"

    def __str__(self): return str(self.name_ru) if self.name_ru else "Без названия"

class ObjectTerritory(models.Model):
    object = models.OneToOneField(AccessibilityObject, on_delete=models.CASCADE, related_name='territory')
    entrance_width_ok = models.BooleanField("Ширина прохода соответствует", default=False)

class EntranceGroup(models.Model):
    object = models.OneToOneField(AccessibilityObject, on_delete=models.CASCADE, related_name='entrance_group')
    has_ramp = models.BooleanField("Наличие пандуса", default=False)

class ObjectPhoto(models.Model):
    object = models.ForeignKey(AccessibilityObject, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField("Фотография", upload_to='objects/%Y/%m/%d/')
    description = models.CharField("Описание фото", max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class SubObject(models.Model):
    parent_object = models.ForeignKey(AccessibilityObject, on_delete=models.CASCADE, related_name='sub_objects')
    name = models.CharField("Название под-объекта", max_length=255)


class BusStop(gis_models.Model):
    sending_status = models.ForeignKey(PassportStatus, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Статус отправки", related_name="stop_status")
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)
    stop_name = models.CharField("Остановка", max_length=255, null=True, blank=True)
    location = gis_models.PointField("Точка координат", srid=4326, null=True, blank=True)
    ownership_type = models.ForeignKey(OwnershipEntity, on_delete=models.PROTECT, null=True, blank=True)
    responsible_body = models.ForeignKey(ResponsibleBody, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = "Паспорт остановки"
        verbose_name_plural = "2. Паспорта остановок"

    def __str__(self): return str(self.stop_name) if self.stop_name else "Остановка без названия"

class StopAccessibility(models.Model):
    stop = models.OneToOneField(BusStop, on_delete=models.CASCADE, related_name='accessibility')
    street_cat = models.ForeignKey(StreetCategory, on_delete=models.SET_NULL, null=True, blank=True)

class StopPlatform(models.Model):
    stop = models.OneToOneField(BusStop, on_delete=models.CASCADE, related_name='platform')
    has_tactile_tile = models.BooleanField("Тактильная плитка", default=False)

class StopPavilion(models.Model):
    stop = models.OneToOneField(BusStop, on_delete=models.CASCADE, related_name='pavilion')
    has_lighting = models.BooleanField("Освещение", default=False)
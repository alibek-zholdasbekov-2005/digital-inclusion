from django.contrib.gis.db import models as gis_models
from django.db import models

class District(gis_models.Model):
    name_ru = models.CharField("Название на русском", max_length=255, null=True, blank=True)
    name_kz = models.CharField("Название на казахском", max_length=255, null=True, blank=True)

    
    gerb = models.ImageField("Герб района", upload_to='districts/logos/', null=True, blank=True)
    akim_name = models.CharField("ФИО Акима", max_length=255, null=True, blank=True)
    
    geometry = gis_models.MultiPolygonField("Границы района (полигон)", srid=4326, null=True, blank=True)
    
    is_deleted = models.BooleanField("Удалено", default=False)

    class Meta:
        verbose_name = "Район города"
        verbose_name_plural = "Районы городов"
        ordering = ['id']

    def __str__(self):
        return self.name_ru if self.name_ru else "Без названия"

class Category(models.Model):
    name_ru = models.CharField("Название (RU)", max_length=255, default='') 
    name_kz = models.CharField("Название (KZ)", max_length=255, blank=True, default='')
    
    icon = models.ImageField("Иконка категории", upload_to='categories/icons/', blank=True, null=True)
    
    color = models.CharField("Цвет маркера (HEX)", max_length=7, default="#2196F3")
    
    sort_order = models.PositiveIntegerField("Порядок сортировки", default=0)

    class Meta:
        verbose_name = "Категория объекта"
        verbose_name_plural = "Категории объектов"
        ordering = ['sort_order', 'name_ru']

    def __str__(self):
        return self.name_ru

class ActivityType(models.Model):
    name_ru = models.CharField("Наименование вида деятельности на русском", max_length=255)
    name_kz = models.CharField("Наименование вида деятельности на казахском", max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Вид деятельности"
        verbose_name_plural = "Виды деятельности"
        ordering = ['-id']

    def __str__(self):
        return self.name_ru 

class AccessibilityCategory(models.Model):
    code = models.CharField("Код", max_length=2, unique=True)
    name_ru = models.CharField("Наименование вида деятельности на русском", max_length=255)
    name_kz = models.CharField("Наименование вида деятельности на казахском", max_length=255, blank=True, null=True)


    class Meta:
        verbose_name = "Категория МГН"
        verbose_name_plural = "Категории МГН"

    def __str__(self):
        return f"{self.code} - {self.name_ru}"
    
class OwnershipEntity(models.Model):
    name = models.CharField("Субъект собственности", max_length=255)
    class Meta:
        verbose_name = "Субъект собственности"
        verbose_name_plural = "5. Субъекты собственности"
    def __str__(self): return self.name

class ResponsibleBody(models.Model):
    name = models.CharField("Ответственный орган", max_length=255)
    class Meta:
        verbose_name = "Ответственный орган"
        verbose_name_plural = "6. Ответственные органы"
    def __str__(self): return self.name

class StreetCategory(models.Model):
    name = models.CharField("Категория улицы", max_length=255)
    class Meta:
        verbose_name = "Категория улицы"
        verbose_name_plural = "7. Категории улицы"
    def __str__(self): return self.name

class PassportStatus(models.Model):
    name = models.CharField("Статус паспорта", max_length=100)
    class Meta:
        verbose_name = "Статус паспорта"
        verbose_name_plural = "8. Статусы паспортов"
    def __str__(self): return self.name

class CoverageCategory(models.Model):
    name = models.CharField("Тип покрытия", max_length=100)
    class Meta:
        verbose_name = "Категория покрытия"
        verbose_name_plural = "9. Категории покрытия"
    def __str__(self): return self.name

class Street(models.Model):
    name = models.CharField("Название улицы", max_length=255)
    class Meta:
        verbose_name = "Улица"
        verbose_name_plural = "10. Улицы"
    def __str__(self): return self.name
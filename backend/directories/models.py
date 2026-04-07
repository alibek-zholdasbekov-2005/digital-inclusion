from django.db import models

class District(models.Model):
    name = models.CharField("Район", max_length=255)
    class Meta:
        verbose_name = "Район"
        verbose_name_plural = "1. Районы"
    def __str__(self): return self.name

class Category(models.Model):
    name = models.CharField("Категория", max_length=255)
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "2. Категории"
    def __str__(self): return self.name

class ActivityType(models.Model):
    name = models.CharField("Вид деятельности", max_length=255)
    class Meta:
        verbose_name = "Вид деятельности"
        verbose_name_plural = "3. Виды деятельности"
    def __str__(self): return self.name

class AccessibilityStatus(models.Model):
    name = models.CharField("Статус доступности", max_length=255)
    class Meta:
        verbose_name = "Доступность объекта"
        verbose_name_plural = "4. Доступность объектов"
    def __str__(self): return self.name

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
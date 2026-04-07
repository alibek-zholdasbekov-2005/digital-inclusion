from django.contrib import admin
from .models import (
    District, Category, ActivityType, 
    AccessibilityStatus, OwnershipEntity, 
    ResponsibleBody, StreetCategory, PassportStatus
)

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin): pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): pass

@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin): pass

@admin.register(AccessibilityStatus)
class AccessibilityStatusAdmin(admin.ModelAdmin): pass

@admin.register(OwnershipEntity)
class OwnershipEntityAdmin(admin.ModelAdmin): pass

@admin.register(ResponsibleBody)
class ResponsibleBodyAdmin(admin.ModelAdmin): pass

@admin.register(StreetCategory)
class StreetCategoryAdmin(admin.ModelAdmin): pass

@admin.register(PassportStatus)
class PassportStatusAdmin(admin.ModelAdmin): pass

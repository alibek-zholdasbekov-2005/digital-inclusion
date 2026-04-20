from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import *

class TerritoryInline(admin.StackedInline): model = ObjectTerritory; extra = 0
class EntranceInline(admin.StackedInline): model = EntranceGroup; extra = 0
class MovementInline(admin.StackedInline): model = MovementWays; extra = 0
class ServiceInline(admin.StackedInline): model = ServiceZones; extra = 0
class SanitaryInline(admin.StackedInline): model = SanitaryRooms; extra = 0
class InfoInline(admin.StackedInline): model = InfoTelecom; extra = 0
class StopAccInline(admin.StackedInline): model = StopAccessibility; extra = 1; classes = ('collapse',)
class StopPlatInline(admin.StackedInline): model = StopPlatform; extra = 1; classes = ('collapse',)
class StopPavInline(admin.StackedInline): model = StopPavilion; extra = 1; classes = ('collapse',)

@admin.register(AccessibilityObject)
class AccessibilityObjectAdmin(LeafletGeoAdmin):
    inlines = [TerritoryInline, EntranceInline, MovementInline, ServiceInline, SanitaryInline, InfoInline]

@admin.register(ObjectAccessibilityResult)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('object', 'section', 'k_status', 'o_status', 'z_status', 's_status')

@admin.register(BusStop)
class BusStopAdmin(LeafletGeoAdmin):
    fieldsets = (
        ('Статусы', {'fields': ('sending_status', 'rejection_reason', 'report_photo'), 'classes': ('collapse',)}),
        ('Инфо', {'fields': ('district', 'stop_name', 'comment', 'not_in_tx')}),
        ('Карта', {'fields': ('location',)}),
        ('Владение', {'fields': ('ownership_type', 'responsible_body')}),
    )
    inlines = [StopAccInline, StopPlatInline, StopPavInline]
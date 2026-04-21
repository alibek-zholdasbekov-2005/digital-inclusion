from rest_framework import serializers
from .models import *
from directories.models import Category

class CategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name_ru', 'icon', 'color']

class TerritorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectTerritory
        fields = '__all__'

class EntranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntranceGroup
        fields = '__all__'

class MovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementWays
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceZones
        fields = '__all__'

class SanitarySerializer(serializers.ModelSerializer):
    class Meta:
        model = SanitaryRooms
        fields = '__all__'

class InfoTelecomSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoTelecom
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectAccessibilityResult
        fields = ['section', 'k_status', 'o_status', 'z_status', 's_status']

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectPhoto
        fields = ['id', 'image']

class ObjectListSerializer(serializers.ModelSerializer):
    category_info = CategoryShortSerializer(source='category', read_only=True)
    district_name = serializers.ReadOnlyField(source='district.name_ru')
    avg_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = AccessibilityObject
        fields = [
            'id', 'name_ru', 'location', 'district', 'district_name',
            'category', 'category_info', 'avg_rating', 'reviews_count',
        ]

    def get_avg_rating(self, obj):
        # Use annotation if present, otherwise fall back to aggregate
        val = getattr(obj, '_avg_rating', None)
        if val is None:
            qs = obj.reviews.all()
            if not qs.exists():
                return None
            val = sum(r.rating for r in qs) / qs.count()
        return round(float(val), 1) if val is not None else None

    def get_reviews_count(self, obj):
        val = getattr(obj, '_reviews_count', None)
        return int(val) if val is not None else obj.reviews.count()

class AccessibilityObjectDetailSerializer(serializers.ModelSerializer):
    territory = TerritorySerializer(read_only=True)
    entrance_group = EntranceSerializer(read_only=True)
    movement_ways = MovementSerializer(read_only=True)
    service_zones = ServiceSerializer(read_only=True)
    sanitary_rooms = SanitarySerializer(read_only=True)
    info_telecom = InfoTelecomSerializer(read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)
    results = ResultSerializer(many=True, read_only=True)

    category_info = CategoryShortSerializer(source='category', read_only=True)
    district_name = serializers.ReadOnlyField(source='district.name_ru')
    avg_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = AccessibilityObject
        fields = '__all__'

    def get_avg_rating(self, obj):
        qs = obj.reviews.all()
        if not qs.exists():
            return None
        return round(sum(r.rating for r in qs) / qs.count(), 1)

    def get_reviews_count(self, obj):
        return obj.reviews.count()

class BusStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStop
        fields = '__all__'
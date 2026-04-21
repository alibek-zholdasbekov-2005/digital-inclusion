from rest_framework import serializers
from django.db import transaction

from .models import (
    AccessibilityObject, ObjectTerritory, EntranceGroup, MovementWays,
    ServiceZones, SanitaryRooms, InfoTelecom, ObjectPhoto,
    ObjectAccessibilityResult, BusStop,
)
from directories.models import Category


SECTION_MODELS = {
    'territory': ObjectTerritory,
    'entrance_group': EntranceGroup,
    'movement_ways': MovementWays,
    'service_zones': ServiceZones,
    'sanitary_rooms': SanitaryRooms,
    'info_telecom': InfoTelecom,
}


class CategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name_ru', 'icon', 'color']


def _section_serializer(model_cls):
    class _S(serializers.ModelSerializer):
        class Meta:
            model = model_cls
            exclude = ('object',)
    _S.__name__ = f'{model_cls.__name__}Serializer'
    return _S


TerritorySerializer = _section_serializer(ObjectTerritory)
EntranceSerializer = _section_serializer(EntranceGroup)
MovementSerializer = _section_serializer(MovementWays)
ServiceSerializer = _section_serializer(ServiceZones)
SanitarySerializer = _section_serializer(SanitaryRooms)
InfoTelecomSerializer = _section_serializer(InfoTelecom)


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
            'category', 'category_info', 'moderation_state',
            'avg_rating', 'reviews_count',
        ]

    def get_avg_rating(self, obj):
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
    territory = TerritorySerializer(required=False, allow_null=True)
    entrance_group = EntranceSerializer(required=False, allow_null=True)
    movement_ways = MovementSerializer(required=False, allow_null=True)
    service_zones = ServiceSerializer(required=False, allow_null=True)
    sanitary_rooms = SanitarySerializer(required=False, allow_null=True)
    info_telecom = InfoTelecomSerializer(required=False, allow_null=True)

    photos = PhotoSerializer(many=True, read_only=True)
    results = ResultSerializer(many=True, read_only=True)

    category_info = CategoryShortSerializer(source='category', read_only=True)
    district_name = serializers.ReadOnlyField(source='district.name_ru')
    created_by_username = serializers.ReadOnlyField(source='created_by.username')
    avg_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = AccessibilityObject
        fields = '__all__'
        read_only_fields = (
            'created_by', 'created_at', 'updated_at',
            'moderation_state', 'rejection_reason',
        )

    def get_avg_rating(self, obj):
        qs = obj.reviews.all()
        if not qs.exists():
            return None
        return round(sum(r.rating for r in qs) / qs.count(), 1)

    def get_reviews_count(self, obj):
        return obj.reviews.count()

    def _pop_sections(self, data):
        return {name: data.pop(name, None) for name in SECTION_MODELS}

    @transaction.atomic
    def create(self, validated_data):
        sections = self._pop_sections(validated_data)
        obj = super().create(validated_data)
        for rel_name, payload in sections.items():
            if payload is not None:
                SECTION_MODELS[rel_name].objects.create(object=obj, **payload)
        return obj

    @transaction.atomic
    def update(self, instance, validated_data):
        sections = self._pop_sections(validated_data)
        instance = super().update(instance, validated_data)
        for rel_name, payload in sections.items():
            if payload is None:
                continue
            model_cls = SECTION_MODELS[rel_name]
            model_cls.objects.update_or_create(object=instance, defaults=payload)
        return instance


class BusStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStop
        fields = '__all__'

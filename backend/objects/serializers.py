from rest_framework import serializers
from .models import AccessibilityObject, ObjectTerritory, EntranceGroup, ObjectPhoto, BusStop

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectPhoto
        fields = ['id', 'image', 'description']

class ObjectDetailSerializer(serializers.ModelSerializer):
    accessibility_status = serializers.ReadOnlyField(source='accessibility_calculation')
    district_name = serializers.ReadOnlyField(source='district.name')
    photos = PhotoSerializer(many=True, read_only=True)
    
    class Meta:
        model = AccessibilityObject
        fields = [
            'id', 'name_ru', 'full_legal_name', 'district_name', 
            'location', 'polygon', 'accessibility_status', 'photos'
        ]

class ObjectListSerializer(serializers.ModelSerializer):
    district_name = serializers.ReadOnlyField(source='district.name')
    class Meta:
        model = AccessibilityObject
        fields = ['id', 'name_ru', 'location', 'district_name']

class BusStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStop
        fields = '__all__'
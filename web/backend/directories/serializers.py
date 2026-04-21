from rest_framework import serializers
from .models import District, Category


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name_ru', 'name_kz']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name_ru', 'name_kz', 'icon', 'color', 'sort_order']

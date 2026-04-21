from rest_framework import viewsets, permissions

from .models import District, Category
from .serializers import DistrictSerializer, CategorySerializer


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    """Районы города Алматы (read-only справочник)."""
    queryset = District.objects.filter(is_deleted=False).order_by('name_ru')
    serializer_class = DistrictSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Категории объектов (read-only справочник)."""
    queryset = Category.objects.all().order_by('sort_order', 'name_ru')
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

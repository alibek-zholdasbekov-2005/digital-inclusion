from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend # Импорт фильтров
from rest_framework import filters # Импорт поиска
from .models import AccessibilityObject
from .serializers import ObjectListSerializer, ObjectDetailSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .documents import AccessibilityObjectDocument
from .serializers import ObjectListSerializer
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from rest_framework.decorators import action
class ObjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AccessibilityObject.objects.all()
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    
    filterset_fields = ['district', 'category']
    
    search_fields = ['full_name', 'address']

    def get_serializer_class(self):
        if self.action == 'list':
            return ObjectListSerializer
        return ObjectDetailSerializer
    @action(detail=False, methods=['get'])
    def nearby(self, request):
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        dist = request.query_params.get('dist', 1000)

        if lat and lon:
            user_location = Point(float(lon), float(lat), srid=4326)
            queryset = AccessibilityObject.objects.filter(
                location__distance_lte=(user_location, float(dist))
            ).annotate(distance=Distance('location', user_location)).order_by('distance')
            
            serializer = ObjectListSerializer(queryset, many=True)
            return Response(serializer.data)
        
        return Response({"error": "Укажите lat и lon"}, status=400)

class ObjectSearchView(APIView):
    def get(self, request):
        q = request.query_params.get('q')
        if q:
            search = AccessibilityObjectDocument.search().query(
                "multi_match", 
                query=q, 
                fields=['name_ru', 'full_legal_name']
            )
            objects = search.to_queryset()
            serializer = ObjectListSerializer(objects, many=True)
            return Response(serializer.data)
        return Response([])
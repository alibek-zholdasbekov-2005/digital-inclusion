from rest_framework import viewsets, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.postgres.search import SearchVector
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .models import AccessibilityObject, BusStop
from .serializers import (
    ObjectListSerializer, 
    AccessibilityObjectDetailSerializer,
    BusStopSerializer
)

class ObjectViewSet(viewsets.ModelViewSet): 
    queryset = AccessibilityObject.objects.all()
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['district', 'category']
    search_fields = ['name_ru', 'full_legal_name']

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return ObjectListSerializer
        return AccessibilityObjectDetailSerializer 

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

class BusStopViewSet(viewsets.ModelViewSet):
    queryset = BusStop.objects.all()
    serializer_class = BusStopSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ObjectSearchView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        q = request.query_params.get('q')
        if q:
            results = AccessibilityObject.objects.annotate(
                search=SearchVector('name_ru', 'full_legal_name'),
            ).filter(search=q)
            
            serializer = ObjectListSerializer(results, many=True)
            return Response(serializer.data)
        return Response([])
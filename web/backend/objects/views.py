from rest_framework import viewsets, permissions, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.postgres.search import SearchVector
from django_filters.rest_framework import DjangoFilterBackend

from .models import AccessibilityObject, BusStop, ObjectPhoto
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    ObjectListSerializer,
    AccessibilityObjectDetailSerializer,
    BusStopSerializer,
    PhotoSerializer,
)


class ObjectViewSet(viewsets.ModelViewSet):
    queryset = AccessibilityObject.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['district', 'category', 'moderation_state']
    search_fields = ['name_ru', 'full_legal_name']
    permission_classes = [IsOwnerOrReadOnly]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_queryset(self):
        qs = AccessibilityObject.objects.all()
        user = self.request.user
        if self.action == 'list':
            # Public listing shows approved passports.
            # Authenticated users additionally see their own work-in-progress.
            if user.is_authenticated and not user.is_staff:
                return qs.filter(
                    moderation_state=AccessibilityObject.MODERATION_APPROVED
                ) | qs.filter(created_by=user)
            if not user.is_staff:
                return qs.filter(moderation_state=AccessibilityObject.MODERATION_APPROVED)
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return ObjectListSerializer
        return AccessibilityObjectDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        dist = request.query_params.get('dist', 1000)

        if lat and lon:
            user_location = Point(float(lon), float(lat), srid=4326)
            qs = self.get_queryset().filter(
                location__distance_lte=(user_location, float(dist))
            ).annotate(distance=Distance('location', user_location)).order_by('distance')
            return Response(ObjectListSerializer(qs, many=True).data)

        return Response({"error": "Укажите lat и lon"}, status=400)

    @action(detail=True, methods=['post'], permission_classes=[IsOwnerOrReadOnly])
    def submit(self, request, pk=None):
        obj = self.get_object()
        if obj.moderation_state == AccessibilityObject.MODERATION_APPROVED:
            return Response(
                {"detail": "Паспорт уже одобрен."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        obj.moderation_state = AccessibilityObject.MODERATION_PENDING
        obj.rejection_reason = ''
        obj.save(update_fields=['moderation_state', 'rejection_reason', 'updated_at'])
        return Response(AccessibilityObjectDetailSerializer(obj, context={'request': request}).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        obj = self.get_object()
        obj.moderation_state = AccessibilityObject.MODERATION_APPROVED
        obj.save(update_fields=['moderation_state', 'updated_at'])
        return Response({'status': obj.moderation_state})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        obj = self.get_object()
        obj.moderation_state = AccessibilityObject.MODERATION_REJECTED
        obj.rejection_reason = request.data.get('reason', '') or ''
        obj.save(update_fields=['moderation_state', 'rejection_reason', 'updated_at'])
        return Response({'status': obj.moderation_state, 'reason': obj.rejection_reason})

    @action(
        detail=True,
        methods=['get', 'post'],
        permission_classes=[IsOwnerOrReadOnly],
        parser_classes=[MultiPartParser, FormParser, JSONParser],
        url_path='photos',
    )
    def photos(self, request, pk=None):
        obj = self.get_object()
        if request.method == 'GET':
            qs = obj.photos.all()
            return Response(PhotoSerializer(qs, many=True).data)

        image = request.FILES.get('image')
        if not image:
            return Response({'image': 'Файл обязателен.'}, status=status.HTTP_400_BAD_REQUEST)
        photo = ObjectPhoto.objects.create(object=obj, image=image)
        return Response(PhotoSerializer(photo).data, status=status.HTTP_201_CREATED)


class BusStopViewSet(viewsets.ModelViewSet):
    queryset = BusStop.objects.all()
    serializer_class = BusStopSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ObjectSearchView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        q = request.query_params.get('q')
        if q:
            results = AccessibilityObject.objects.filter(
                moderation_state=AccessibilityObject.MODERATION_APPROVED
            ).annotate(
                search=SearchVector('name_ru', 'full_legal_name'),
            ).filter(search=q)
            return Response(ObjectListSerializer(results, many=True).data)
        return Response([])

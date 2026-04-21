from rest_framework import viewsets, generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import ForumTopic, ForumPost, Review, Favorite
from django.contrib.auth.models import User
from .serializers import (
    ForumTopicSerializer,
    ForumPostSerializer,
    ReviewSerializer,
    UserSerializer,
    FavoriteSerializer,
)
from .auth_serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class ForumTopicViewSet(viewsets.ModelViewSet):
    queryset = ForumTopic.objects.filter(is_archived=False).order_by('-created_at')
    serializer_class = ForumTopicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ForumPostViewSet(viewsets.ModelViewSet):
    queryset = ForumPost.objects.all().order_by('created_at')
    serializer_class = ForumPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['topic']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['object']
    ordering_fields = ['rating', 'created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class UserProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class FavoriteViewSet(viewsets.ModelViewSet):
    """Избранные объекты текущего пользователя."""
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['object']

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
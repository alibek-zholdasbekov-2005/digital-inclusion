from rest_framework import viewsets, generics, permissions
from .models import ForumTopic, ForumPost, Review
from django.contrib.auth.models import User
from .serializers import ForumTopicSerializer, ForumPostSerializer, ReviewSerializer
from .auth_serializers import RegisterSerializer

# Представление для регистрации
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

# Темы форума
class ForumTopicViewSet(viewsets.ModelViewSet):
    queryset = ForumTopic.objects.filter(is_archived=False).order_by('-created_at')
    serializer_class = ForumTopicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Сообщения форума (ТОТ САМЫЙ КЛАСС)
class ForumPostViewSet(viewsets.ModelViewSet):
    queryset = ForumPost.objects.all().order_by('created_at')
    serializer_class = ForumPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Отзывы
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
from rest_framework import serializers
from .models import ForumTopic, ForumPost, Review
from django.contrib.auth.models import User

class ForumPostSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = ForumPost
        fields = ['id', 'topic', 'author', 'author_name', 'text', 'image', 'created_at']

class ForumTopicSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    posts_count = serializers.IntegerField(source='posts.count', read_only=True)
    class Meta:
        model = ForumTopic
        fields = ['id', 'title', 'author', 'author_name', 'created_at', 'is_archived', 'posts_count']

class ReviewSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Review
        fields = ['id', 'object', 'author', 'author_name', 'rating', 'text', 'photo', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
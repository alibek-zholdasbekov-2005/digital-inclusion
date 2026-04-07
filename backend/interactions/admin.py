from django.contrib import admin
from .models import ForumTopic, ForumPost, Review, Favorite

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'object', 'created_at')
    list_filter = ('user',)

@admin.register(ForumTopic)
class ForumTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_archived')

@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('topic', 'author', 'created_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('object', 'author', 'rating', 'created_at')
    list_filter = ('rating',)

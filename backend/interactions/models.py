from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from objects.models import AccessibilityObject

class ForumTopic(models.Model):
    title = models.CharField("Тема обсуждения", max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Тема форума"
        verbose_name_plural = "Форум: Темы"

    def __str__(self):
        return self.title

class ForumPost(models.Model):
    topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField("Сообщение")
    image = models.ImageField("Изображение", upload_to='forum/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Сообщение форума"
        verbose_name_plural = "Форум: Сообщения"

class Review(models.Model):
    object = models.ForeignKey(AccessibilityObject, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField("Оценка (1-5)", validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField("Текст отзыва")
    photo = models.ImageField("Фото к отзыву", upload_to='reviews/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы и оценки"

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    object = models.ForeignKey(AccessibilityObject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'object')
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные объекты"


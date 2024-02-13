from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    content = models.TextField(verbose_name='Контент')
    image = models.ImageField(verbose_name='Малюнок', upload_to='post_images/')
    is_published = models.BooleanField(verbose_name='Опубліковано', default=False)
    likes = models.IntegerField(verbose_name='Вподобайки', default=0)
    views = models.IntegerField(verbose_name='Перегляди', default=0)
    created_at = models.DateTimeField(verbose_name='Дата створення', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата оновлення', auto_now=True)
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости'
        ordering = ['-created_at']
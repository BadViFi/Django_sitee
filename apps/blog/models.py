import os
import uuid

from django.db import models
from django.contrib.auth.models import User
from django.core.files import File

from io import BytesIO
from PIL import Image


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='posts', null=True, default=None)
        
    title = models.CharField(verbose_name='Заголовок', max_length=255,blank=False)
    content = models.TextField(verbose_name='Контент',blank=False)
    image = models.ImageField(verbose_name='Малюнок', upload_to='post_images/',default="linux",blank=True)
    image_thumbnail = models.ImageField(verbose_name='Мініатюра', upload_to='post_images/', blank=True)
    is_published = models.BooleanField(verbose_name='Опубліковано', default=False,blank=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    dis_likes = models.IntegerField(verbose_name='Огидайки', default=0,blank=True)
    views = models.IntegerField(verbose_name='Перегляди', default=0,blank=True)
    created_at = models.DateTimeField(verbose_name='Дата створення', auto_now_add=True,blank=True)
    updated_at = models.DateTimeField(verbose_name='Дата оновлення', auto_now=True,blank=True)
    
    
    def __str__(self):
        return f'{self.title} - {self.created_at} - {self.is_published}'
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости'
        ordering = ['-created_at']
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)     
        if self.image:
            self.make_thumbnail(self.image)
            super().save(*args, **kwargs)
                
    def get_thumbnail(self):
        if self.image_thumbnail:
            return self.image_thumbnail.url
        else:
            if self.image:
                self.image_thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.image_thumbnail.url
            else:
                return 'https://via.placeholder.com/240x240x.jpg'
    
    def make_thumbnail(self, image, size=(820, 440)):
        img = Image.open(image)
        img.convert('RGBA')
        img.thumbnail(size)
        img = img.resize(size, Image.LANCZOS)

        thumb_io = BytesIO()
        img.save(thumb_io, 'PNG', quality=85)
        name = image.name.replace('post_images/', 'thumbnails/')
        thumbnail = File(thumb_io, name=name)

        return thumbnail
        
        
        
        
        
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост', related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='comments', null=True, default=None)
    content = models.TextField(verbose_name='Контент')
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    created_at = models.DateTimeField(verbose_name='Дата створення', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата оновлення', auto_now=True)
    
    def __str__(self):
        return f'{self.author} - {self.created_at}'
    
    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'
        ordering = ['created_at']
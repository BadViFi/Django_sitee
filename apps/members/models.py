from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(verbose_name='Аватар', upload_to='avatars/', default='avatars/default.png')
    bio = models.TextField(verbose_name='Біографія', blank=True)
    birth_date = models.DateField(verbose_name='Дата народження', null=True, blank=True)
    location = models.CharField(verbose_name='Місце проживання', max_length=255, blank=True)
    website = models.URLField(verbose_name='Веб-сайт', blank=True)
    phone = models.CharField(verbose_name='Телефон', max_length=15, blank=True)
    
    def get_avatar(self):
        if self.avatar == '/avatars/default.png':
            return self.avatar.url
        #static avatar/default.png
        return '/static/avatars/default.png'
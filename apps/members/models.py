from django.db import models
from django.contrib.auth.models import User

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from ckeditor.fields import RichTextField


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(verbose_name='Аватар', upload_to='avatars/', default='avatars/default.png')
    avatar_thumbnail = ImageSpecField(source='avatar',
                                      processors=[ResizeToFill(300, 300)],
                                      format='JPEG',
                                      options={'quality': 60})
    bio = RichTextField(verbose_name='Біографія', max_length=200, blank=True)
    birth_date = models.DateField(verbose_name='Дата народження', null=True, blank=True)
    location = models.CharField(verbose_name='Місце проживання', max_length=255, blank=True)
    website = models.URLField(verbose_name='Веб-сайт', blank=True)
    phone = models.CharField(verbose_name='Телефон', max_length=15, blank=True)
    is_private = models.BooleanField(verbose_name='Приватний профіль', default=False)
    
    followers = models.ManyToManyField(User, related_name='following', blank=True)

    def follow(self, user):
        self.followers.add(user)

    def unfollow(self, user):
        self.followers.remove(user)

    def is_following(self, user):#
        return user in self.followers.all()

    def get_followers(self):
        return self.followers.all()
    def get_following(self):
        print(Profile.objects.filter(followers=self.user))
        return Profile.objects.filter(followers__in=[self.user])
    
    def get_avatar(self):
        if self.avatar:
            return self.avatar_thumbnail.url
        return '/media/avatars/default.png'
    
    def __str__(self):
        return f'{self.user.username}'
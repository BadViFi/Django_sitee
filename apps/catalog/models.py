import uuid

from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from mptt.models import MPTTModel, TreeForeignKey

from imagekit.models import  ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class Catalog(MPTTModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name='Назва')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Опис', null=True)
    image = ProcessedImageField(
        verbose_name='Зображення',
        upload_to='catalog/',
        processors=[ResizeToFill(820, 440)],
        format='JPEG',
        options={'quality': 60},
        blank=True,
        null=True
    )
    parent = TreeForeignKey(
        to='self',
        on_delete=models.CASCADE,
        related_name='child',
        blank=True,
        null=True,
    )
    
    def __str__(self):
        full_path = [self.name]
        parent = self.parent
        while parent is not None:
            full_path.append(parent.name)
            parent = parent.parent
        return ' -> '.join(full_path[::-1])
    
    def get_absolute_url(self):
        return reverse("catalog:category", kwargs={"slug": self.slug})
    
    def image_tag_thumbnail(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" height="70" />')
        
    image_tag_thumbnail.short_description = 'Зображення'
    image_tag_thumbnail.allow_tags = True
    
    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" />')
    image_tag.short_description = 'Зображення'
    image_tag.allow_tags = True
    
    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['name']
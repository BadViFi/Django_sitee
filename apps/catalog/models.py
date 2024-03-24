import uuid

from django.contrib.admin import display
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from mptt.models import MPTTModel, TreeForeignKey

from imagekit.models import  ProcessedImageField, ImageSpecField
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
        
        
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name='Назва')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Опис', null=True)
    quantity = models.PositiveIntegerField(verbose_name='Кількість', default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    category = models.ManyToManyField(
        to=Catalog,
        related_name='products',
        through='ProductCategory',
        verbose_name='Категорії',
        blank=True,
    )
    
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'
        ordering = ['-created_at']
        
        
    def __str__(self):
        return self.name
    
    
    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"slug": self.slug})
    
    def images(self):
        return Image.objects.filter(product=self.id)
    
    def main_image(self):
        image = Image.objects.filter(product=self.id, is_main=True).first()
        if image:
            return image
        return self.images().first()
        
    def main_category(self):
        category = self.category.filter(category__productcategory__is_main=True).first() #вибираємо категорію, яка є основною
        if category:
            return category
        return self.category.first()
    
    @display(description='Ціна')
    def price_display(self):
        return f'{self.price} грн.'
    
    @display(description='Основне зображення')
    def image_tag(self):
        image = self.main_image()
        if image:
            return mark_safe(f'<img src="{image.image_thumbnail.url}" />')
    
    

class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    category = models.ForeignKey(Catalog, on_delete=models.CASCADE, verbose_name='Категорія')
    is_main = models.BooleanField(default=False, verbose_name='Основна категорія')
    
    def __str__(self):
        return f'{self.product.name} -> {self.category.name}'
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.is_main:
            ProductCategory.objects.filter(product=self.product, is_main=True).update(is_main=False)
        super().save(force_insert, force_update, using, update_fields)
        
    class Meta:
        verbose_name = 'Категорія товару'
        verbose_name_plural = 'Категорії товарів'
        
        
class Image(models.Model):
    image = ProcessedImageField(
        verbose_name='Зображення',
        upload_to='catalog/products/',
        processors=[],
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True
    )
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(300, 200)],
        format='JPEG',
        options={'quality': 60}
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Товар'
    )
    is_main = models.BooleanField(default=False, verbose_name='Основне зображення')
    
    
    @display(description='Зображення')
    def image_tag_thumbnail(self):
        if self.image:
            return mark_safe(f'<img src="{self.image_thumbnail.url}" height="70" />')
        
    @display(description='Основне зображення')
    def image_tag(self):
        if self.image:
            return mark_safe(f'<img src="{self.image_thumbnail.url}" />')
from django.contrib import admin

from .models import Catalog, Product,Image


class ProductCategoryInline(admin.TabularInline):
    model = Product.category.through
    extra = 1

class ImageInline(admin.TabularInline):
    model = Image
    fields = ('product', 'image_tag_thumbnail', 'image', 'is_main')
    readonly_fields = ('image_tag_thumbnail',)
    extra = 1



@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_tag_thumbnail', 'is_main')
    readonly_fields = ('image_tag',)

# Register your models here.
@admin.register(Catalog)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag_thumbnail')
    prepopulated_fields = {'slug': ('name',)} # це поле автоматично заповнюється на основі іншого поля
    readonly_fields = ('image_tag_thumbnail',) # це поле тільки для читання
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_display', 'created_at', 'updated_at', 'image_tag')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductCategoryInline, ImageInline]
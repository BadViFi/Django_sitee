from django.contrib import admin

from .models import Catalog

# Register your models here.
@admin.register(Catalog)
class CategoryAdmin(admin.ModelAdmin):
    # list_display = ('name', 'image_tag_thumbnail')
    prepopulated_fields = {'slug': ('name',)} # це поле автоматично заповнюється на основі іншого поля
    # readonly_fields = ('image_tag_thumbnail',) # це поле тільки для читання
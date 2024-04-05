from django.contrib import admin

from .models import Cart
# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    list_filter = ('user', 'product')
    search_fields = ('user', 'product')
    list_per_page = 10
    list_display_links = ('user', 'product')
    list_editable = ('quantity',) # Які поля можна редагувати прямо зі списку
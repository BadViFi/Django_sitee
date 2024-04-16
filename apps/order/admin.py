from django.contrib import admin

from .models import Cart,Order,OrderProduct
# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    list_filter = ('user', 'product')
    search_fields = ('user', 'product')
    list_per_page = 10
    list_display_links = ('user', 'product')
    list_editable = ('quantity',) # Які поля можна редагувати прямо зі списку


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    fields = ('product', 'quantity', 'price')
    readonly_fields = ('product', 'quantity', 'price')
    editable_fields = ('quantity', 'price')



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'created_at', 'status', 'paid')
    list_filter = ('user', 'status')
    search_fields = ('user', 'status')
    list_per_page = 10
    list_display_links = ('user', 'total_price')
    list_editable = ('status', 'paid') # Які поля можна редагувати прямо зі списку
    inlines = [OrderProductInline]
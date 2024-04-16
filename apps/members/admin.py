from django.contrib import admin
from .models import Profile


# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'avatar', 'bio', 'birth_date', 'location', 'website', 'phone']
    list_display = ['user', 'avatar', 'bio', 'birth_date', 'location', 'website', 'phone']
    list_filter = ['user', 'birth_date']
    search_fields = ['user', 'bio', 'location', 'website', 'phone']
    list_per_page = 10
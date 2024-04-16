from django.contrib import admin

from .models import Post, Comment

# Register your models here.
@admin.register(Post) # Це потрібно для відображення моделі в адмінці
class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'is_published', 'image', 'author']
    list_display = ['title', 'content', 'is_published', 'image', 'author']
    list_filter = ['is_published', 'author']
    search_fields = ['title', 'content', 'author']
    list_per_page = 10

admin.site.register(Comment) # Це потрібно для відображення моделі в адмінці
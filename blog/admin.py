from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """
    Настройка отображения блоговых записей в админке
    """
    list_display = ('id', 'title', 'created_at', 'is_published', 'views_count')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'views_count')
    list_editable = ('is_published',)
    list_display_links = ('id', 'title')

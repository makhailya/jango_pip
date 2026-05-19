from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Настройка отображения категорий в админке
    """
    list_display = ('id', 'name', 'description')
    search_fields = ('name', 'description')
    list_display_links = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Настройка отображения продуктов в админке
    """
    list_display = ('id', 'name', 'price', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    list_display_links = ('id', 'name')

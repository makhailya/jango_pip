from django.core.cache import cache
from django.conf import settings
from .models import Product, Category


def get_products_by_category(category_id):
    """
    Сервисная функция для получения продуктов по категории

    Args:
        category_id (int): ID категории

    Returns:
        QuerySet: Список продуктов в категории
    """
    if settings.CACHE_ENABLED:
        # Формируем ключ кеша
        cache_key = f'products_category_{category_id}'

        # Пробуем получить из кеша
        products = cache.get(cache_key)

        if products is None:
            # Если в кеше нет, получаем из БД
            products = list(
                Product.objects.filter(
                    category_id=category_id,
                    is_published=True
                ).select_related('category', 'owner')
            )

            # Сохраняем в кеш на 5 минут
            cache.set(cache_key, products, 60 * 5)

        return products
    else:
        # Если кеш отключен, просто возвращаем из БД
        return Product.objects.filter(
            category_id=category_id,
            is_published=True
        ).select_related('category', 'owner')


def get_all_products():
    """
    Сервисная функция для получения всех опубликованных продуктов

    Returns:
        QuerySet: Список всех опубликованных продуктов
    """
    if settings.CACHE_ENABLED:
        cache_key = 'all_products'

        products = cache.get(cache_key)

        if products is None:
            products = list(
                Product.objects.filter(
                    is_published=True
                ).select_related('category', 'owner')
            )

            # Кешируем на 5 минут
            cache.set(cache_key, products, 60 * 5)

        return products
    else:
        return Product.objects.filter(
            is_published=True
        ).select_related('category', 'owner')


def get_all_categories():
    """
    Получить все категории с кешированием

    Returns:
        QuerySet: Список категорий
    """
    if settings.CACHE_ENABLED:
        cache_key = 'all_categories'

        categories = cache.get(cache_key)

        if categories is None:
            categories = list(Category.objects.all())

            # Кешируем на 10 минут
            cache.set(cache_key, categories, 60 * 10)

        return categories
    else:
        return Category.objects.all()


def clear_product_cache():
    """
    Очистить кеш продуктов
    Вызывается при создании/изменении/удалении продукта
    """
    if settings.CACHE_ENABLED:
        cache.delete('all_products')
        # Очищаем кеш для всех категорий
        categories = Category.objects.all()
        for category in categories:
            cache.delete(f'products_category_{category.id}')

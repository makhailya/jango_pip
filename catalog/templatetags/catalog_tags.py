from django import template
from catalog.services import get_all_categories

register = template.Library()


@register.simple_tag
def get_categories():
    """
    Template tag для получения всех категорий
    Использует кеширование

    Использование в шаблоне:
        {% load catalog_tags %}
        {% get_categories as categories %}
        {% for category in categories %}
            {{ category.name }}
        {% endfor %}
    """
    return get_all_categories()

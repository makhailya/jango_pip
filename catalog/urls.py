from django.urls import path
from . import views

# Это пространство имён для приложения
# Позволяет использовать {% url 'catalog:home' %} в шаблонах
app_name = 'catalog'

urlpatterns = [
    # Главная страница: /
    path('', views.home, name='home'),

    # Страница контактов: /contacts/
    path('contacts/', views.contacts, name='contacts'),
]
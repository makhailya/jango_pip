from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),

    # Страница одного товара
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    # Страница контактов
    path('contacts/', views.contacts, name='contacts'),
]

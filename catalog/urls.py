from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Главная страница
    path('', views.HomeView.as_view(), name='home'),

    # Страница одного товара
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),

    # Страница контактов
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
]
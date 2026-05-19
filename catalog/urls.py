from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Главная страница
    path('', views.HomeView.as_view(), name='home'),

    # Страница одного товара
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),

    # Продукты в категории
    path('category/<int:pk>/', views.CategoryProductsView.as_view(), name='category_products'),

    # Создание продукта
    path('product/create/', views.ProductCreateView.as_view(), name='product_create'),

    # Редактирование продукта
    path('product/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),

    # Удаление продукта
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    # Переключение публикации (для модераторов)
    path('product/<int:pk>/toggle-publish/', views.TogglePublishView.as_view(), name='toggle_publish'),

    # Страница контактов
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
]

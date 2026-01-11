from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Админ-панель Django
    path('admin/', admin.site.urls),
    
    # Подключаем URLs приложения catalog
    # Все адреса из catalog/urls.py будут доступны по корневому пути
    path('', include('catalog.urls')),
]

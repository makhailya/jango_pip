from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Админ-панель Django
    path('admin/', admin.site.urls),

    # Подключаем URLs приложения catalog
    path('', include('catalog.urls')),

    # Подключаем URLs приложения blog
    path('blogs/', include('blog.urls')),

    # Подключаем URLs приложения users
    path('users/', include('users.urls')),
]

# Добавляем возможность отображать медиафайлы в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

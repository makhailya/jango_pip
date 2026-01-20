from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Список всех статей
    path('', views.BlogListView.as_view(), name='list'),

    # Просмотр отдельной статьи
    path('<int:pk>/', views.BlogDetailView.as_view(), name='detail'),

    # Создание новой статьи
    path('create/', views.BlogCreateView.as_view(), name='create'),

    # Редактирование статьи
    path('<int:pk>/update/', views.BlogUpdateView.as_view(), name='update'),

    # Удаление статьи
    path('<int:pk>/delete/', views.BlogDeleteView.as_view(), name='delete'),
]

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Регистрация
    path('register/', views.RegisterView.as_view(), name='register'),

    # Вход
    path('login/', views.UserLoginView.as_view(), name='login'),

    # Выход
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]

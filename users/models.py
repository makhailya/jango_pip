from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


class User(AbstractUser):
    """
    Кастомная модель пользователя
    Использует email для авторизации вместо username
    """
    username = None  # Отключаем username

    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        help_text='Введите адрес электронной почты'
    )
    avatar = models.ImageField(
        upload_to='users/avatars/',
        verbose_name='Аватар',
        help_text='Загрузите фото профиля',
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length=35,
        verbose_name='Номер телефона',
        help_text='Введите номер телефона',
        blank=True,
        null=True
    )
    country = models.CharField(
        max_length=100,
        verbose_name='Страна',
        help_text='Введите страну',
        blank=True,
        null=True
    )

    # Используем email для авторизации
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Убираем обязательные поля кроме email и password

    # Используем кастомный менеджер
    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']

    def __str__(self):
        return self.email

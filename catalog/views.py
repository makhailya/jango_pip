from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db import models
from .models import Product, Category
from .forms import ProductForm
from .services import get_products_by_category, get_all_products, clear_product_cache


class HomeView(ListView):
    """
    Контроллер главной страницы
    Использует низкоуровневое кеширование через сервисную функцию
    """
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        """
        Используем сервисную функцию с кешированием
        """
        # Если пользователь не авторизован, показываем только опубликованные
        if not self.request.user.is_authenticated:
            return get_all_products()

        # Если авторизован, показываем опубликованные + свои
        user = self.request.user
        if user.groups.filter(name='Модераторы').exists() or user.is_superuser:
            return Product.objects.all()

        # Для обычных пользователей - опубликованные + свои
        return Product.objects.filter(
            models.Q(is_published=True) | models.Q(owner=user)
        )


@method_decorator(cache_page(60 * 15), name='dispatch')  # Кеш на 15 минут
class ProductDetailView(DetailView):
    """
    Контроллер страницы одного товара
    Доступен всем пользователям для опубликованных товаров
    Страница кешируется на 15 минут
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        """
        Показываем опубликованные товары всем
        Неопубликованные - только владельцу и модераторам
        """
        queryset = Product.objects.all()

        if not self.request.user.is_authenticated:
            return queryset.filter(is_published=True)

        user = self.request.user
        if user.groups.filter(name='Модераторы').exists() or user.is_superuser:
            return queryset

        return queryset.filter(
            models.Q(is_published=True) | models.Q(owner=user)
        )


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер создания продукта
    Автоматически привязывает продукт к текущему пользователю
    Очищает кеш после создания
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        """
        Автоматически устанавливаем владельца продукта
        """
        form.instance.owner = self.request.user
        response = super().form_valid(form)

        # Очищаем кеш после создания продукта
        clear_product_cache()

        return response


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Контроллер редактирования продукта
    Доступен только владельцу продукта
    Очищает кеш после изменения
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def test_func(self):
        """
        Проверка: пользователь должен быть владельцем продукта
        """
        product = self.get_object()
        return product.owner == self.request.user

    def form_valid(self, form):
        """
        Очищаем кеш после изменения
        """
        response = super().form_valid(form)
        clear_product_cache()
        return response

    def get_success_url(self):
        """
        После редактирования перенаправляем на страницу просмотра товара
        """
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Контроллер удаления продукта
    Доступен владельцу и модераторам
    Очищает кеш после удаления
    """
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
    context_object_name = 'product'

    def test_func(self):
        """
        Проверка: пользователь должен быть владельцем или модератором
        """
        product = self.get_object()
        user = self.request.user

        # Владелец может удалять
        if product.owner == user:
            return True

        # Модератор может удалять
        if user.groups.filter(name='Модераторы').exists():
            return True

        # Суперпользователь может удалять
        if user.is_superuser:
            return True

        return False

    def form_valid(self, form):
        """
        Очищаем кеш после удаления
        """
        response = super().form_valid(form)
        clear_product_cache()
        return response


class TogglePublishView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Контроллер для переключения статуса публикации
    Доступен только модераторам
    """
    model = Product

    def test_func(self):
        """
        Проверка: пользователь должен иметь право на отмену публикации
        """
        return (
                self.request.user.has_perm('catalog.can_unpublish_product') or
                self.request.user.is_superuser
        )

    def post(self, request, *args, **kwargs):
        """
        Переключаем статус публикации
        """
        product = self.get_object()
        product.is_published = not product.is_published
        product.save()
        return redirect('catalog:product_detail', pk=product.pk)


class ContactsView(TemplateView):
    """
    Контроллер страницы контактов
    """
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        """
        Обработка POST-запроса (отправка формы)
        """
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        print(f"Получено сообщение от {name} ({email}): {message}")

        context = self.get_context_data()
        context['form_submitted'] = True
        return self.render_to_response(context)


class CategoryProductsView(ListView):
    """
    Контроллер для отображения продуктов в категории
    Использует сервисную функцию с кешированием
    """
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        """
        Получаем продукты через сервисную функцию
        """
        category_id = self.kwargs.get('pk')
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        """
        Добавляем категорию в контекст
        """
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('pk')
        context['category'] = Category.objects.get(pk=category_id)
        return context

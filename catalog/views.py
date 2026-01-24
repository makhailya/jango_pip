from django.db import models
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from .models import Product
from .forms import ProductForm


class HomeView(ListView):
    """
    Контроллер главной страницы
    Отображает список всех опубликованных продуктов
    """
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        """
        Обычные пользователи видят только опубликованные продукты
        Владельцы и модераторы видят все свои продукты
        """
        queryset = Product.objects.all()

        # Если пользователь не авторизован, показываем только опубликованные
        if not self.request.user.is_authenticated:
            return queryset.filter(is_published=True)

        # Если пользователь авторизован, показываем:
        # - Все опубликованные продукты
        # - Свои неопубликованные продукты
        # - Если модератор - все продукты
        user = self.request.user
        if user.groups.filter(name='Модераторы').exists() or user.is_superuser:
            return queryset

        return queryset.filter(
            models.Q(is_published=True) | models.Q(owner=user)
        )


class ProductDetailView(DetailView):
    """
    Контроллер страницы одного товара
    Доступен всем пользователям для опубликованных товаров
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
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Контроллер редактирования продукта
    Доступен только владельцу продукта
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

    def get_success_url(self):
        """
        После редактирования перенаправляем на страницу просмотра товара
        """
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Контроллер удаления продукта
    Доступен владельцу и модераторам
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
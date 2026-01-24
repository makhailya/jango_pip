from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product
from .forms import ProductForm


class HomeView(ListView):
    """
    Контроллер главной страницы
    Отображает список всех продуктов
    """
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    """
    Контроллер страницы одного товара
    Доступен всем пользователям
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер создания продукта
    Доступен только авторизованным пользователям
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер редактирования продукта
    Доступен только авторизованным пользователям
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        """
        После редактирования перенаправляем на страницу просмотра товара
        """
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер удаления продукта
    Доступен только авторизованным пользователям
    """
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
    context_object_name = 'product'


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
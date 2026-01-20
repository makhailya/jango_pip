from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Product


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
    """
    model = Product
    template_name = 'catalog/product_detail.html'
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

        # Добавляем контекст для отображения сообщения об успехе
        context = self.get_context_data()
        context['form_submitted'] = True
        return self.render_to_response(context)
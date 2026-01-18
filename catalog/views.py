from django.shortcuts import render, get_object_or_404
from .models import Product


def home(request):
    """
    Контроллер главной страницы
    Отображает список всех продуктов из базы данных
    """
    # Получаем все продукты из БД
    products = Product.objects.all()

    context = {
        'products': products
    }
    return render(request, 'catalog/home.html', context)


def product_detail(request, pk):
    """
    Контроллер страницы одного товара

    Args:
        pk (int): Primary key (ID) товара

    Returns:
        Отрендеренный шаблон с данными товара
    """
    # Получаем товар по ID или возвращаем 404
    product = get_object_or_404(Product, pk=pk)

    context = {
        'product': product
    }
    return render(request, 'catalog/product_detail.html', context)


def contacts(request):
    """
    Контроллер страницы контактов
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        print(f"Получено сообщение от {name} ({email}): {message}")

        context = {
            'form_submitted': True
        }
        return render(request, 'catalog/contacts.html', context)

    return render(request, 'catalog/contacts.html')

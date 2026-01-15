from django.shortcuts import render


def home(request):
    """
    Контроллер главной страницы

    Эта функция обрабатывает запрос на главную страницу
    и возвращает отрендеренный HTML-шаблон
    """
    return render(request, 'catalog/home.html')


def contacts(request):
    """
    Контроллер страницы контактов

    Обрабатывает GET и POST запросы:
    - GET: показывает форму
    - POST: обрабатывает отправку формы
    """
    # Проверяем, была ли отправлена форма (POST-запрос)
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Выводим данные в консоль (для проверки)
        print(f"Получено сообщение от {name} ({email}): {message}")

        # Передаём флаг, что форма отправлена
        context = {
            'form_submitted': True
        }
        return render(request, 'catalog/contacts.html', context)

    # Если обычный GET-запрос, просто показываем форму
    return render(request, 'catalog/contacts.html')


from django.shortcuts import render

# Create your views here.

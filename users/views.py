from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.conf import settings
from .forms import UserRegisterForm, UserLoginForm
from .models import User


class RegisterView(CreateView):
    """
    Контроллер регистрации пользователя
    """
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """
        Переопределяем метод для отправки приветственного письма
        """
        # Сохраняем пользователя
        response = super().form_valid(form)

        # Получаем email нового пользователя
        user_email = form.cleaned_data.get('email')

        # Отправляем приветственное письмо
        send_mail(
            subject='Добро пожаловать в наш интернет-магазин!',
            message=f'Здравствуйте!\n\nСпасибо за регистрацию в нашем интернет-магазине.\n\nВаш email: {user_email}\n\nТеперь вы можете войти в систему и начать делать покупки!\n\nС уважением,\nКоманда интернет-магазина',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )

        return response


class UserLoginView(LoginView):
    """
    Контроллер авторизации пользователя
    """
    form_class = UserLoginForm
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    """
    Контроллер выхода пользователя
    """
    pass

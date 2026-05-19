from django import forms
from django.core.exceptions import ValidationError
from .models import Product

# Список запрещённых слов (в нижнем регистре)
FORBIDDEN_WORDS = [
    'казино',
    'криптовалюта',
    'крипта',
    'биржа',
    'дешево',
    'бесплатно',
    'обман',
    'полиция',
    'радар',
]


class ProductForm(forms.ModelForm):
    """
    Форма для создания и редактирования продукта
    """

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price', 'is_published']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Введите название продукта'
            }),
            'description': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Введите описание продукта'
            }),
            'price': forms.NumberInput(attrs={
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы со стилизацией
        """
        super().__init__(*args, **kwargs)

        # Добавляем Bootstrap классы ко всем полям
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                # Для чекбоксов (если будут)
                field.widget.attrs['class'] = 'form-check-input'
            else:
                # Для остальных полей
                field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        """
        Валидация поля name на запрещённые слова
        """
        name = self.cleaned_data.get('name')

        if name:
            # Приводим к нижнему регистру для проверки
            name_lower = name.lower()

            # Проверяем каждое запрещённое слово
            for forbidden_word in FORBIDDEN_WORDS:
                if forbidden_word in name_lower:
                    raise ValidationError(
                        f'Название не может содержать запрещённое слово: "{forbidden_word}"'
                    )

        return name

    def clean_description(self):
        """
        Валидация поля description на запрещённые слова
        """
        description = self.cleaned_data.get('description')

        if description:
            # Приводим к нижнему регистру для проверки
            description_lower = description.lower()

            # Проверяем каждое запрещённое слово
            for forbidden_word in FORBIDDEN_WORDS:
                if forbidden_word in description_lower:
                    raise ValidationError(
                        f'Описание не может содержать запрещённое слово: "{forbidden_word}"'
                    )

        return description

    def clean_price(self):
        """
        Валидация поля price - цена не может быть отрицательной
        """
        price = self.cleaned_data.get('price')

        if price is not None and price < 0:
            raise ValidationError(
                'Цена не может быть отрицательной. Пожалуйста, введите положительное значение.'
            )

        return price

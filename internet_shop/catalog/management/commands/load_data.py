from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product


class Command(BaseCommand):
    """
    Кастомная команда для загрузки тестовых данных

    Использование:
        python manage.py load_data
    """
    help = 'Загружает тестовые данные из фикстур'

    def handle(self, *args, **options):
        """
        Основной метод команды
        """
        self.stdout.write(self.style.WARNING('Начинается загрузка данных...'))

        # Шаг 1: Удаление существующих данных
        self.stdout.write('Удаление существующих данных...')
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('✓ Данные удалены'))

        # Шаг 2: Загрузка категорий
        self.stdout.write('Загрузка категорий...')
        call_command('loaddata', 'categories.json')
        categories_count = Category.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'✓ Загружено категорий: {categories_count}')
        )

        # Шаг 3: Загрузка продуктов
        self.stdout.write('Загрузка продуктов...')
        call_command('loaddata', 'products.json')
        products_count = Product.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'✓ Загружено продуктов: {products_count}')
        )

        # Шаг 4: Проверка связей
        self.stdout.write('\nПроверка связей:')
        for category in Category.objects.all():
            count = category.products.count()
            self.stdout.write(
                f'  • {category.name}: {count} продукт(ов)'
            )

        self.stdout.write(
            self.style.SUCCESS('\n✓ Данные успешно загружены!')
        )

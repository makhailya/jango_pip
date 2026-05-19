from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    """
    Команда для создания групп и настройки прав доступа

    Использование:
        python manage.py create_groups
    """
    help = 'Создаёт группы и настраивает права доступа'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Создание групп и настройка прав...'))

        # Получаем ContentType для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # === Группа "Модераторы" ===
        moderators_group, created = Group.objects.get_or_create(name='Модераторы')

        if created:
            self.stdout.write(self.style.SUCCESS('✓ Группа "Модераторы" создана'))
        else:
            self.stdout.write('  Группа "Модераторы" уже существует')

        # Получаем разрешения
        permissions = []

        # 1. Кастомное разрешение на отмену публикации
        can_unpublish = Permission.objects.get(
            codename='can_unpublish_product',
            content_type=content_type
        )
        permissions.append(can_unpublish)
        self.stdout.write('  → Добавлено право: Может отменять публикацию продукта')

        # 2. Разрешение на удаление продукта
        can_delete = Permission.objects.get(
            codename='delete_product',
            content_type=content_type
        )
        permissions.append(can_delete)
        self.stdout.write('  → Добавлено право: Может удалять продукт')

        # 3. Разрешение на просмотр продукта
        can_view = Permission.objects.get(
            codename='view_product',
            content_type=content_type
        )
        permissions.append(can_view)
        self.stdout.write('  → Добавлено право: Может просматривать продукт')

        # 4. Разрешение на изменение продукта
        can_change = Permission.objects.get(
            codename='change_product',
            content_type=content_type
        )
        permissions.append(can_change)
        self.stdout.write('  → Добавлено право: Может изменять продукт')

        # Устанавливаем разрешения для группы
        moderators_group.permissions.set(permissions)

        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Группа "Модераторы" настроена с {len(permissions)} правами')
        )

        # Выводим итоговую информацию
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('Настройка завершена!'))
        self.stdout.write('=' * 60)
        self.stdout.write('\nДоступные группы:')
        for group in Group.objects.all():
            perms = group.permissions.count()
            self.stdout.write(f'  • {group.name}: {perms} прав(а)')

        self.stdout.write('\nДля добавления пользователя в группу:')
        self.stdout.write('  1. Зайдите в админку: /admin/')
        self.stdout.write('  2. Откройте пользователя')
        self.stdout.write('  3. В разделе "Groups" выберите "Модераторы"')
        self.stdout.write('  4. Сохраните\n')

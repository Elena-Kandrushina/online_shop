from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Создает группу и назначает права.'

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Модератор продуктов')
        if created:
            permission = Permission.objects.get(codename='can_unpublish_product')
            permission_delete = Permission.objects.get(codename='can_delete_product')
            group.permissions.add(permission, permission_delete)
            self.stdout.write(self.style.SUCCESS('Группа создана и права добавлены.'))
        else:
            self.stdout.write(self.style.WARNING('Группа уже существует.'))
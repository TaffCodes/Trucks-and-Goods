# core/management/commands/create_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Truck, Driver, Trip

class Command(BaseCommand):
    help = 'Create user groups and assign permissions'

    def handle(self, *args, **kwargs):
        # Define groups
        groups = {
            'Admin': {
                'permissions': Permission.objects.all(),
            },
            'Fleet Manager': {
                'permissions': [
                    'add_trip', 'change_trip', 'delete_trip', 'view_trip',
                    'add_driver', 'change_driver', 'delete_driver', 'view_driver',
                    'add_truck', 'change_truck', 'delete_truck', 'view_truck',
                ],
            },
            'Driver': {
                'permissions': [
                    'view_trip', 'change_trip',
                ],
            },
            'Client': {
                'permissions': [
                    'view_trip',
                ],
            },
        }

        for group_name, group_data in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" created'))
            else:
                self.stdout.write(self.style.WARNING(f'Group "{group_name}" already exists'))

            for perm_codename in group_data['permissions']:
                try:
                    perm = Permission.objects.get(codename=perm_codename)
                    group.permissions.add(perm)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Permission "{perm_codename}" not found'))

            group.save()
            self.stdout.write(self.style.SUCCESS(f'Permissions assigned to group "{group_name}"'))
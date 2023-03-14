from django.core.management.base import BaseCommand
from customer.models import Customer

# This command is used to activate the user using the activate and id input
# from the command line, and deactivate the user using the deactivate and id 
# input from the command line.

class Command(BaseCommand):
    help = 'Activate or deactivate a user'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str)
        parser.add_argument('id', type=int)

    def handle(self, *args, **kwargs):
        action = kwargs['action']
        id = kwargs['id']
        user = Customer.objects.get(id=id)
        if action == 'activate':
            user.is_active = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f'User {user.email} activated'))
        elif action == 'deactivate':
            user.is_active = False
            user.save()
            self.stdout.write(self.style.SUCCESS(f'User {user.email} deactivated'))
        else:
            self.stdout.write(self.style.ERROR(f'Invalid action'))
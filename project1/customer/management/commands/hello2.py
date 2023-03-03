from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Prints a welcome message'

    # Take input from user and print it
    def add_arguments(self, parser):
        parser.add_argument('name', type=str)

    def handle(self, *args, **kwargs):
        name = kwargs['name']
        self.stdout.write(self.style.SUCCESS(f'Hello {name}'))

    
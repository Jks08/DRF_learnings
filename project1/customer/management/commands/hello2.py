from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Prints a welcome message'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Hello JKS'))
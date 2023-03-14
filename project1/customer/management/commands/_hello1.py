# This file begins with an underscore to prevent it from being run as a command.
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Prints error'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Hello Error'))
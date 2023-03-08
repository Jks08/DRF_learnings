import json
import datetime
from django.core.management.base import BaseCommand
from kbapp.models import AMC

class Command(BaseCommand):
    help = 'Load AMC data from json file'

    def load_data_to_amc(self, data):
        pass

    def handle(self, *args, **kwargs):
        file = open('project1/jsons/AMC.json', 'r')
        return "Blank"
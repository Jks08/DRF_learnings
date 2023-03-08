import json
import datetime
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from kbapp.models import AMC

class Command(BaseCommand):
    help = 'Load AMC data from json file to database'

    def load_data_to_amc(self, data):
        json_data = json.load(data)
        self.stdout.write(f'JSON data: {json_data}')

        rta_amc_code = json_data['fields']['rta_amc_code']
        # self.stdout.write(f'rta_amc_code: {rta_amc_code}')
        obj = AMC.objects.filter(rta_amc_code=rta_amc_code).first()

        try:
            if obj:
                for key, value in json_data['fields'].items():
                    setattr(obj, key, value)
                obj.modified_by = "Admin User"
                obj.modified = datetime.datetime.now()
                obj.save()
                self.stdout.write(self.style.SUCCESS(f'Updated AMC: {obj.name}'))

            else:
                obj_new = AMC(**json_data['fields'])
                obj_new.created_by = "Admin User"
                obj_new.created = datetime.datetime.now()
                obj_new.save()
                self.stdout.write(self.style.SUCCESS(f'Created AMC: {obj_new.name}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))

        # Show the updated databse records
        for obj in AMC.objects.all():
            self.stdout.write(f'All AMCs: {obj.name}')
        # pass

    def handle(self, *args, **kwargs):
        filepath = os.path.join(os.path.dirname(settings.BASE_DIR) + '/project1/jsons/AMC.json')
        file = open(filepath, 'r')
        self.load_data_to_amc(file)
        file.close()
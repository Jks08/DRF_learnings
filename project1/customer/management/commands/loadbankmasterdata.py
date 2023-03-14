from django.core.management import BaseCommand
from customer.models import Customer, BankMaster, CustomerBankAccount

# This command is used to load the bank master data from the csv file
# into the database. If the bank already exists in the database, then
# it will not be added again, but the details will be updated. 
# If the bank does not exist in the database, then it will be added.

class Command(BaseCommand):
    help = 'Load bank master data to table BankMaster'

    def handle(self, *args, **kwargs):
        path = '/Users/jishnusrivastava/Desktop/MyMy/project1/customer/static/databases/bank_master_data.csv'
        with open(path, 'r') as f:
            for line in f.readlines()[1:]:
                bank_id, bank_name, bank_website, bank_logo, bank_number = line.split(',')
                try:
                    bank_object = BankMaster.objects.get(bank_id=bank_id)
                    bank_object.bank_name = bank_name
                    bank_object.bank_website = bank_website
                    bank_object.bank_logo = bank_logo
                    bank_object.bank_number = bank_number
                    bank_object.save()
                    self.stdout.write(self.style.WARNING(f'Updated following: {bank_id, bank_name, bank_website, bank_logo, bank_number}'))
                except BankMaster.DoesNotExist:
                    bank_object = BankMaster.objects.create(bank_id=bank_id, bank_name=bank_name, bank_website=bank_website, bank_logo=bank_logo,bank_number=bank_number)
                    self.stdout.write(self.style.SUCCESS(f'Created {bank_name} with the following details\n: {bank_id, bank_name, bank_website, bank_logo, bank_number}'))




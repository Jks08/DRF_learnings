from django.core.management import BaseCommand
from customer.models import Customer, BankMaster, CustomerBankAccount

# This command is used to load the bank master data from the csv file
# into the database. If the bank already exists in the database, then
# it will not be added again. If the bank does not exist in the database,
# then it will be added.

class Command(BaseCommand):
    help = 'Load bank master data'

    def handle(self, *args, **kwargs):
        path = '/Users/jishnusrivastava/Desktop/MyMy/project1/customer/static/databases/bank_master_data.csv'
        with open(path, 'r') as f:
            for line in f.readlines()[1:]:
                bank_id, bank_name, bank_website, bank_logo, bank_number = line.split(',')
                try:
                    bank_object = BankMaster.objects.get(bank_id=bank_id)
                    self.stdout.write(f'Got {bank_name}')
                except:
                    bank_object = BankMaster.objects.create(bank_id=bank_id, bank_name=bank_name, bank_website=bank_website, bank_logo=bank_logo,bank_number=bank_number)
                    self.stdout.write(f'Created {bank_name}')


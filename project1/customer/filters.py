import django_filters
from customer.models import CustomerBankAccount, Customer

class CustomerFilter(django_filters.FilterSet):
    # email = django_filters.CharFilter(lookup_expr='icontains')
    # first_name = django_filters.CharFilter(lookup_expr='icontains')
    # last_name = django_filters.CharFilter(lookup_expr='icontains')
    # pan_no = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Customer
        fields = ['email', 'first_name', 'last_name', 'pan_no']
    
    fields = {
            'email': ['exact', 'contains'],
            'first_name': ['exact', 'contains'],
            'last_name': ['exact', 'contains'],
            'pan_no': ['exact', 'contains']
        }

class CustomerBankAccountFilter(django_filters.FilterSet):
    account_number = django_filters.CharFilter(lookup_expr='icontains')
    ifsc_code = django_filters.CharFilter(lookup_expr='icontains')
    name_as_per_bank_record = django_filters.CharFilter(lookup_expr='icontains')
    account_type = django_filters.CharFilter(lookup_expr='icontains')
    bank__bank_name = django_filters.CharFilter(lookup_expr='icontains')
    bank__bank_id = django_filters.CharFilter(lookup_expr='icontains')
    bank__bank_website = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = CustomerBankAccount
        fields = ['account_number', 'ifsc_code', 'name_as_per_bank_record', 'account_type', 'bank__bank_name', 'bank__bank_id', 'bank__bank_website']
from django.conf import settings
from rest_framework import serializers
from customer.models import Customer, BankMaster, CustomerBankAccount
from django.conf import settings


from typing import Dict
import os

User = Customer

class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id','email', 'first_name', 'middle_name', 'last_name', 'pan_no', 'password')

    def create(self, validated_data: Dict[str, any]) -> User:
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user
    
class BankMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankMaster
        fields = '__all__'

class CustomerBankAccountSerializer(serializers.ModelSerializer):
    bank_logo = serializers.CharField(source='bank.bank_logo', read_only=True)
    bank_name = serializers.CharField(source='bank.bank_name', read_only=True)
    customer_first_name = serializers.CharField(source='customer.first_name', read_only=True)
    customer_last_name = serializers.CharField(source='customer.last_name', read_only=True)
    customer_email = serializers.CharField(source='customer.email', read_only=True)

    class Meta:
        model = CustomerBankAccount
        fields = ['created_by','id',"account_number","ifsc_code", "customer","customer_first_name","customer_last_name","customer_email", "name_as_per_bank_record","bank", 'bank_name',"bank_logo", "cheque_image", "branch_name", "account_type","is_active", "verification_status"]

    def to_representation(self, instance: CustomerBankAccount) -> Dict[str, any]:
        representation = super().to_representation(instance)
        bank = instance.bank
        customer = instance.customer
        logo = bank.bank_logo

        if logo:
            representation['bank_logo'] = os.path.join(settings.MEDIA_ROOT, logo.url)

        bank_name = bank.bank_name
        representation['bank_name'] = bank_name

        first_name = customer.first_name
        last_name = customer.last_name
        email = customer.email
        representation['customer_first_name'] = first_name
        representation['customer_last_name'] = last_name
        representation['customer_email'] = email
        return representation
        
    def validate_number_of_accounts(self, attrs: Dict[str, any]) -> Dict[str, any]:
        if CustomerBankAccount.objects.filter(customer=attrs['customer']).count() >= settings.MAX_ACCOUNTS_PER_CUSTOMER:
            raise serializers.ValidationError(f"You can only add max of {settings.MAX_ACCOUNTS_PER_CUSTOMER} accounts.")
        return attrs
    
    def validate_set_current_account_as_active(self, attrs: Dict[str, any]) -> Dict[str, any]:
        if CustomerBankAccount.objects.filter(customer=attrs['customer'], is_active=True):
            CustomerBankAccount.objects.filter(customer=attrs['customer']).update(is_active=False)
        attrs['is_active'] = True
        return attrs
    
    def validate_account_number_and_ifsc_code(self, attrs: Dict[str, any]) -> Dict[str, any]:
        if CustomerBankAccount.objects.filter(account_number=attrs['account_number'], ifsc_code=attrs['ifsc_code']).count() >= 1:
            raise serializers.ValidationError("Account number and IFSC code already exists.")
        return attrs

    def validate(self, attrs: Dict[str, any]) -> Dict[str, any]:
        if not self.instance:
            attrs['customer'] = self.context['request'].user
            account_number = attrs.get('account_number')
            ifsc_code = attrs.get('ifsc_code')

            existing_customer = CustomerBankAccount.activate_existing_account(account_number, ifsc_code, attrs['customer'])
            if existing_customer:
                self.instance = existing_customer

            else:
                self.validate_number_of_accounts(attrs)
                self.validate_set_current_account_as_active(attrs)
                self.validate_account_number_and_ifsc_code(attrs)

        return super().validate(attrs)
    
    def update(self, instance: CustomerBankAccount, validated_data: Dict[str, any]) -> CustomerBankAccount:
        if instance.is_active:
            if instance.verification_status != 'Verified':
                instance.ifsc_code = validated_data.get('ifsc_code', instance.ifsc_code)
                instance.branch_name = validated_data.get('branch_name', instance.branch_name)
                instance.name_as_per_bank_record = validated_data.get('name_as_per_bank_record', instance.name_as_per_bank_record)
                instance.account_type = validated_data.get('account_type', instance.account_type)
                instance.save()
                return instance
            else:
                raise serializers.ValidationError("Account is already verified. You cannot update it.")
        else:
            raise serializers.ValidationError("Account is not active. You cannot update it.")
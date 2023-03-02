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

    class Meta:
        model = CustomerBankAccount
        fields = ['id',"account_number","ifsc_code", "customer", "bank", "cheque_image", "branch_name", "name_as_per_bank_record","account_type","is_active", "bank_logo", "verification_status"]

    def to_representation(self, instance: CustomerBankAccount) -> Dict[str, any]:
        representation = super().to_representation(instance)
        bank = instance.bank
        logo = bank.bank_logo
        if logo:
            representation['bank_logo'] = os.path.join(settings.MEDIA_ROOT, logo.url)
        return representation

    def validate_existing_account(self, attrs: Dict[str, any]) -> Dict[str, any]:
        attrs['customer'] = self.context['request'].user
        existing_accounts  = CustomerBankAccount.objects.filter(
            customer=attrs['customer'],
            ifsc_code = attrs['ifsc_code'],
            account_number = attrs['account_number'],
        ).first()

        if existing_accounts:
            existing_account = existing_accounts
            CustomerBankAccount.objects.filter(customer=attrs['customer'], is_active=True).update(is_active=False)
            existing_account.is_active = True
            existing_account.save()
            attrs['id'] = existing_account.id
            attrs['is_active'] = True
            return attrs
        
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

            # Use validate_existing_account method to check if account already exists
            existing_account = self.validate_existing_account(attrs)
            if existing_account:
                return existing_account
            else:
                # Use validate_number_of_accounts method to check if max number of accounts is reached
                self.validate_number_of_accounts(attrs)
                # Use validate_set_current_account_as_active method to set current account as active
                self.validate_set_current_account_as_active(attrs)
                # Use validate_account_number_and_ifsc_code method to check if account number and ifsc code already exists
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
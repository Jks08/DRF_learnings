from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from customer.models import Customer, BankMaster, CustomerBankAccount
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

    def validate(self, attrs: Dict[str, any]) -> Dict[str, any]:
        if not self.instance:
            attrs['customer'] = self.context['request'].user
            if CustomerBankAccount.objects.filter(customer=attrs['customer']).count() >= 4:
                raise serializers.ValidationError("You can only add maximum 4 accounts.")
        
            if CustomerBankAccount.objects.filter(customer=attrs['customer'], bank=attrs['bank']).count() >= 1:
                raise serializers.ValidationError("You can only add one account per bank.")
            
            if CustomerBankAccount.objects.filter(customer=attrs['customer'], is_active=True):
                CustomerBankAccount.objects.filter(customer=attrs['customer']).update(is_active=False)
            attrs['is_active'] = True

            if CustomerBankAccount.objects.filter(account_number=attrs['account_number'], ifsc_code=attrs['ifsc_code']).count() >= 1:
                raise serializers.ValidationError("Account number and IFSC code already exists.")
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
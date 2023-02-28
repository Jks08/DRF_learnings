from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from customer.models import Customer, BankMaster, CustomerBankAccount

User = Customer

class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id','email', 'first_name', 'middle_name', 'last_name', 'pan_no', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user
    
class BankMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankMaster
        fields = '__all__'

class CustomerBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerBankAccount
        fields = ["account_number","ifsc_code", "customer", "bank", "cheque_image", "branch_name", "name_as_per_bank_record","account_type","is_active"]

    def validate(self, attrs):
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
    
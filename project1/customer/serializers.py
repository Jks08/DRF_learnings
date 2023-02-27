from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from customer.models import Customer, BankMaster, CustomerBankAccount

User = Customer

class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'middle_name', 'last_name', 'pan_no', 'password')

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
        fields = ["account_number","ifsc_code", "customer", "bank", "cheque_image", "branch_name", "name_as_per_bank_record","account_type"]

        def create(self, validated_data):
            customer = validated_data.get('customer')
            if CustomerBankAccount.objects.filter(customer=customer).count() >= 4:
                raise serializers.ValidationError("You can only add maximum 4 accounts.")
            if CustomerBankAccount.objects.filter(customer=customer, is_active=True).count() >= 1 and validated_data.get('is_active'):
                raise serializers.ValidationError("You can only have one active account.")
            if CustomerBankAccount.objects.filter(customer=customer, pan=validated_data.get('pan')).count() >= 4:
                raise serializers.ValidationError("You can only add maximum 4 accounts per PAN.")
            return super().create(validated_data)

        def update(self, instance, validated_data):
            customer = validated_data.get('customer')
            if CustomerBankAccount.objects.filter(customer=customer).exclude(id=instance.id).count() >= 4:
                raise serializers.ValidationError("You can only add maximum 4 accounts.")
            if CustomerBankAccount.objects.filter(customer=customer, is_active=True).exclude(id=instance.id).count() >= 1 and validated_data.get('is_active'):
                raise serializers.ValidationError("You can only have one active account.")
            if CustomerBankAccount.objects.filter(customer=customer, pan=validated_data.get('pan')).exclude(id=instance.id).count() >= 4:
                raise serializers.ValidationError("You can only add maximum 4 accounts per PAN.")
            return super().update(instance, validated_data)
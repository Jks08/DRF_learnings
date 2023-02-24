from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from customer.models import Customer, BankMaster, CustomerBankAccount

User = get_user_model()

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
    bank = BankMasterSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)
    class Meta:
        model = CustomerBankAccount
        fields = '__all__'
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework.authtoken.models import Token
from django.db import transaction, IntegrityError
from rest_framework import serializers

# Create your models here.

class CustomerManager(BaseUserManager):
    def create_user(self, email: str, password: str=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Customer(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    pan_no = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    username = None
    token = models.OneToOneField(Token, on_delete=models.CASCADE, null=True, blank=True)

    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'pan_no']

    def create_token(self) -> Token:
        token = Token.objects.create(user=self)
        self.token = token
        self.save()
        return token

    def __str__(self) -> str:
        return self.email

    def get_full_name(self) -> str:
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self) -> str:
        return self.first_name

class BankMaster(models.Model):
    bank_id = models.AutoField(primary_key=True)
    bank_name = models.CharField(max_length=100)
    bank_website = models.URLField(max_length=200, blank=True, null=True)
    bank_number = models.CharField(max_length=20, blank=True, null=True)
    bank_logo = models.ImageField(upload_to='bank_logo', blank=True, null=True)

    def __str__(self) -> str:
        return self.bank_name
    
class CustomerBankAccount(models.Model):
    account_number = models.CharField(max_length=20, primary_key=False)
    ifsc_code = models.CharField(max_length=11)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    bank = models.ForeignKey(BankMaster, on_delete=models.CASCADE, related_name='bank_accounts')
    cheque_image = models.ImageField(upload_to='cheque_images', blank=True, null=True)
    branch_name = models.CharField(max_length=100)
    is_cheque_verified = models.BooleanField(default=False)
    name_as_per_bank_record = models.CharField(max_length=100)
    verification_mode = models.CharField(choices=(('Manual', 'Manual'), ('OCR', 'OCR')), default='Manual', max_length=20) 
    verification_status = models.CharField(choices=(('Pending', 'Pending'), ('Verified', 'Verified'), ('Rejected', 'Rejected')), default='Pending', max_length=20)
    account_type = models.CharField(choices=(('Savings', 'Savings'), ('Current', 'Current')), max_length=20)
    is_active = models.BooleanField(default=True)

    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['account_number', 'ifsc_code'], name='unique_account_number_ifsc_code')
        ]

    @classmethod
    def activate_existin_account(cls, account_number, ifsc_code, customer):
        existing_customer = cls.objects.filter(customer=customer)
        existing_accounts = existing_customer.filter(account_number=account_number, ifsc_code=ifsc_code)
        if existing_accounts:
            existing_account = existing_accounts[0]
            existing_account.is_active = True
            existing_account.save(update_fields=['is_active'])

            cls.objects.filter(customer=customer).exclude(id=existing_account.id).update(is_active=False)
            return existing_account
        return None
    
    def save(self, *args, **kwargs):
        try:
            with transaction.atomic():
                super().save(*args, **kwargs)
        except IntegrityError:
            existing_account = self.activate_existin_account(self.account_number, self.ifsc_code, self.customer)
            if existing_account:
                return existing_account
        
    
    def __str__(self) -> str:
        return self.account_number
    
    def account_number_ifsc_code(self) -> str:
        try:
            return self.ifsc_code +'_'+self.account_number
        except CustomerBankAccount.DoesNotExist:
            return None
        


        

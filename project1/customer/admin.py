from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from customer.models import Customer, CustomerBankAccount, BankMaster
from project1.logging import my_function

# Register your models here.

class CustomerAdmin(BaseUserAdmin):
    model = Customer
    ordering = ['email']
    list_display = ['email', 'first_name', 'middle_name', 'last_name', 'pan_no', 'is_active']
    search_fields = ['email', 'first_name', 'last_name', 'pan_no']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'middle_name', 'last_name', 'pan_no')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'middle_name', 'last_name', 'pan_no', 'is_active', 'is_staff')}
        ),
    )
    my_function()

admin.site.register(Customer, CustomerAdmin)

@admin.register(BankMaster)
class BankMasterAdmin(admin.ModelAdmin):
    list_display = ['bank_id', 'bank_name', 'bank_website', 'bank_logo','bank_number']
    search_fields = ['bank_id', 'bank_name', 'bank_website', 'bank_number']
    ordering = ['bank_id']
    my_function()

@admin.register(CustomerBankAccount)
class CustomerBankAccountAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'ifsc_code', 'account_number_ifsc_code', 'customer', 'bank', 'branch_name', 'name_as_per_bank_record', 'account_type']
    search_fields = ['account_number', 'ifsc_code', 'customer', 'bank', 'branch_name']
    ordering = ['account_number']
    my_function()

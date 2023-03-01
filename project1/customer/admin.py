from django.contrib import admin
from django.forms import ModelForm
from django.http.request import HttpRequest
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from customer.models import Customer, CustomerBankAccount, BankMaster
from typing import List

# Register your models here.

class NoPermissionAdmin(admin.ModelAdmin):
    actions = None

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return False
    
    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False
    
    def get_actions(self, request: HttpRequest) -> dict:
        actions = super().get_actions(request)
        actions.clear()
        return actions
    
    def get_readonly_fields(self, request: HttpRequest, obj=None) -> List[str]:
        return [f.name for f in self.model._meta.fields]
    

class CustomerAdmin(NoPermissionAdmin):
    model = Customer
    ordering = ['email']
    list_display = ['id','email', 'first_name', 'middle_name', 'last_name', 'pan_no', 'is_active']
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

admin.site.register(Customer, CustomerAdmin)

@admin.register(BankMaster)
class BankMasterAdmin(admin.ModelAdmin):
    list_display = ['bank_id', 'bank_name', 'bank_website', 'bank_logo','bank_number']
    search_fields = ['bank_id', 'bank_name', 'bank_website', 'bank_number']
    ordering = ['bank_id']

@admin.register(CustomerBankAccount)
class CustomerBankAccountAdmin(NoPermissionAdmin):
    list_display = ['id','account_number', 'ifsc_code', 'account_number_ifsc_code', 'customer', 'bank', 'is_active', 'branch_name', 'name_as_per_bank_record', 'account_type', 'verification_status']
    search_fields = ['account_number', 'ifsc_code', 'customer', 'bank', 'branch_name']
    ordering = ['account_number']

    def save_model(self, request: HttpRequest, obj, form, change: bool) -> None:
        if not change:  
            if CustomerBankAccount.objects.filter(customer=obj.customer).count() >= 4:
                raise Exception("You can only add maximum 4 accounts.")
            if CustomerBankAccount.objects.filter(customer=obj.customer, is_active=True).count() >= 1 and obj.is_active:
                raise Exception("You can only have one active account.")
            
        if change and obj.is_active:
            if CustomerBankAccount.objects.filter(customer=obj.customer, is_active=True).exclude(id=obj.id).count() >= 1:
                raise Exception("You can only have one active account.")
        super().save_model(request, obj, form, change)
        pass


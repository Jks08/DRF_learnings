from django.contrib import admin
from kbapp.models import AMC

# Register your models here.

class AMCAdmin(admin.ModelAdmin):
    model = AMC
    # list_display = ['amc_id','name','rta_amc_code','is_being_sold','is_active']
    # print all column names from AMC model without using model._meta.fields
    # for field in AMC._meta.fields:
        # list_display.append(field.name)
    list_display = [field.name for field in AMC._meta.fields]
admin.site.register(AMC, AMCAdmin)
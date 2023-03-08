from django.contrib import admin
from kbapp.models import AMC

# Register your models here.

class AMCAdmin(admin.ModelAdmin):
    model = AMC
    list_display = ['amc_id','name','rta_amc_code','is_being_sold','is_active']

admin.site.register(AMC, AMCAdmin)
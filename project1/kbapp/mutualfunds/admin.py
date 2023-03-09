from django.contrib import admin
from kbapp.models import AMC, AMCFund

# Register your models here.

class AMCAdmin(admin.ModelAdmin):
    model = AMC
    list_display = [field.name for field in AMC._meta.fields]
admin.site.register(AMC, AMCAdmin)

class AMCFundAdmin(admin.ModelAdmin):
    model = AMCFund
    list_display = [field.name for field in AMCFund._meta.fields]

admin.site.register(AMCFund, AMCFundAdmin)
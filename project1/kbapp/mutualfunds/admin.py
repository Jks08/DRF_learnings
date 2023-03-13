from django.contrib import admin
from kbapp.models import AMC
from kbapp.models import AMCFund, AMCFundScheme

# Register your models here.

class AMCAdmin(admin.ModelAdmin):
    model = AMC
    list_display = [field.name for field in AMC._meta.fields]
admin.site.register(AMC, AMCAdmin)

class AMCFundAdmin(admin.ModelAdmin):
    model = AMCFund
    list_display = [field.name for field in AMCFund._meta.fields]

admin.site.register(AMCFund, AMCFundAdmin)

class AMCFundSchemeAdmin(admin.ModelAdmin):
    model = AMCFundScheme
    list_display = [field.name for field in AMCFundScheme._meta.fields]

admin.site.register(AMCFundScheme, AMCFundSchemeAdmin)
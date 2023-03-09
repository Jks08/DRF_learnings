from django.db import models
import datetime

from base.models import BaseField

# Create your models here.

class AMC(BaseField):
    amc_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True, blank=True, null=True)
    amfi_nav_download_dropdown_code = models.IntegerField(blank=True, null=True, unique=True)
    amc_assets_under_management = models.FloatField(default=0.0, blank=True, null=True)
    amc_aum_date = models.DateTimeField(null=True, blank=True)
    description = models.CharField(max_length=200, default='', blank=True, null=True)
    is_being_sold = models.BooleanField(null=True, default=False)
    f_amc_code = models.CharField(max_length=3, blank=True, null=True)
    # amc_logo = models.ImageField(upload_to='amc_logos', blank=True, null=True)
    amc_logo = models.CharField(max_length=200, blank=True, null=True)
    amc_website_url = models.URLField(blank=True, null=True)
    scheme_information_document_url = models.URLField(blank=True, null=True)
    nominee_url = models.URLField(blank=True, null=True)
    expense_ratio_url = models.URLField(blank=True, null=True)
    expense_ratio_url_remarks = models.CharField(max_length=200, blank=True, null=True, default='')
    last_nav_pull_date_from_amfi  = models.DateTimeField(null=True, blank=True)
    rta_amc_code = models.CharField(max_length=64, blank=True, null=True)
    is_isip_available = models.BooleanField(default=False)
    cio = models.CharField(max_length=150, blank=True, null=True)
    ceo = models.CharField(max_length=150, blank=True, null=True)
    management_trustee = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    owner_type = models.CharField(max_length=50, blank=True, null=True)
    address1 = models.CharField(max_length=200, blank=True, null=True)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    address3 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    pin = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'kbapp_amc'

class AMCFund(BaseField):
    amcfund_id = models.AutoField(primary_key=True)
    rta_fund_code = models.CharField(max_length=10, unique=True, default="NULL")
    name = models.CharField(max_length=255)
    fund_type = models.CharField(max_length=100, null=True, blank=True)
    fund_category = models.CharField(max_length=100, null=True, blank=True)
    fund_sub_type = models.CharField(max_length=100, null=True, blank=True)
    risk_factor = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(max_length=1024, default='N.A', blank=True)
    assets_under_management = models.FloatField(default=0.0, blank=True, null=True)
    assets_under_management_date = models.DateField(null=True, blank=True)
    launch_date = models.DateField(null=True, blank=True)
    is_being_sold = models.BooleanField(null=True, default=True)
    direct_advantage_savings = models.FloatField(default=0.0, max_length=20, null=True, blank=True)
    smart_savings = models.FloatField(default=0.0, max_length=20, null=True, blank=True)
    exit_load_codes = models.CharField(null=True, max_length=128, blank=True)
    fund_class = models.CharField(max_length=64, null=True, blank=True)
    fund_type_id = models.SmallIntegerField(null=True, blank=True)
    scheme_information_document_url = models.URLField(blank=True, null=True)
    amcfund_rating = models.PositiveIntegerField(default=0, null=True, blank=True)
    direct_plan_expense_ratio_in_perc = models.FloatField(default=0.0, null=True, blank=True)
    regular_plan_expense_ratio_in_perc = models.FloatField(null=True, blank=True)
    expense_ratio_as_on_date = models.DateField(null=True, blank=True)
    fund_manager = models.CharField(max_length=64, blank=True, null=True)
    fund_objective = models.TextField(max_length=512, blank=True, null=True)
    fund_manager_since = models.DateField(null=True, blank=True)
    turn_over_ratio = models.FloatField(default=0.0, null=True, blank=True)
    turn_over_ratio_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.name) + str(self.rta_fund_code)
    
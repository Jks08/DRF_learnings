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
    AMC = models.ForeignKey(AMC, on_delete=models.CASCADE, default=1)
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
    
    @classmethod
    def store_fund_data(cls, payload, data):
        payload = payload
        for fund in data['data']['funds']:
            obj = cls.objects.filter(rta_fund_code=fund['scheme']).first()
            if obj:
                for key, val in payload.items():
                    setattr(obj, key, fund[val])
                obj.modified_by = "Admin User"
                obj.modified = datetime.datetime.now()
                obj.save()
            else:
                obj_new = cls()
                for key, val in payload.items():
                    setattr(obj_new, key, fund[val])
                obj_new.created_by = "Admin User"
                obj_new.created = datetime.datetime.now()
                obj_new.save()

class AMCFundScheme(BaseField):
    SWITCH_ALLOWED_CHOICE = (('Y', 'Yes'), ('N', 'No'))
    SWP_ALLOWED_CHOICE = (('Y', 'Yes'), ('N', 'No'))
    STP_ALLOWED_CHOICE = (('Y', 'Yes'), ('N', 'No'))
    SIP_ALLOWED_CHOICE = (('Y', 'Yes'), ('N', 'No'))
    NFO_CHOICES = (('Y', 'Yes'), ('N', 'No'))

    AMCFund = models.ForeignKey(AMCFund, on_delete=models.CASCADE)
    amcfundscheme_id = models.AutoField(primary_key=True)
    name = models.CharField(default='', max_length=200, unique=True)
    rta_amc_code = models.CharField(max_length=200, null=True, blank=True)
    rta_scheme_code = models.CharField(max_length=30,null=True,blank=True, unique=True)
    rta_rta_scheme_code = models.CharField(max_length=20, null=True, blank=True)
    rta_amc_scheme_code = models.CharField(max_length=20, null=True, blank=True)
    rta_plan_code = models.CharField(max_length=20, null=True, blank=True)
    rta_scheme_plan = models.CharField(max_length=25, null=True, blank=True)
    rta_option_code = models.CharField(max_length=20, null=True, blank=True)
    rta_scheme_option = models.CharField(max_length=50, blank=True, null=True)
    rta_scheme_active_flag = models.CharField(max_length=1, null=True, blank=True)
    nfo_start_date = models.DateField(null=True, blank=True)
    nfo_end_date = models.DateField(default=datetime.date(2099, 1, 1))
    rta_purchase_cutoff_time = models.TimeField(null=True, blank=True)
    rta_redemption_cutoff_time = models.TimeField(null=True, blank=True)
    rta_purchase_allowed = models.CharField(max_length=2, null=True, blank=True)
    is_being_sold = models.BooleanField(null=True, default=False)
    rta_redemption_allowed = models.CharField(max_length=2, null=True, blank=True)
    rta_switch_flag = models.CharField(max_length=1,choices=SWITCH_ALLOWED_CHOICE, default='N')
    rta_swp_flag = models.CharField(max_length=1, choices=SWP_ALLOWED_CHOICE, default='N')
    rta_stp_flag = models.CharField(max_length=1, choices=STP_ALLOWED_CHOICE, default='N')
    rta_sip_flag = models.CharField(max_length=1, choices=SIP_ALLOWED_CHOICE, default='N')
    rta_isin = models.CharField(max_length=15, null=True, blank=True)
    nfo_face_value = models.IntegerField(default=0)
    amfi_scheme_code = models.IntegerField(default=0, blank=True, null=True)
    nfo_reopening_date = models.DateField(blank=True, null=True)
    is_nfo = models.CharField(max_length=1, choices=NFO_CHOICES, null=True, blank=True)
    rta_minimum_purchase_amount = models.IntegerField(null=True, blank=True)
    rta_additional_purchase_amount_multiple = models.FloatField(max_length=20, null=True, blank=True)
    rta_redemption_amount_minimum = models.FloatField(max_length=20, null=True, blank=True)

    is_direct_fund = models.BooleanField(null=True, default=False)
    is_regular_fund = models.BooleanField(null=True, default=False)
    is_growth_fund = models.BooleanField(null=True, default=False)
    is_div_payout_fund = models.BooleanField(null=True, default=False)
    is_div_reinvestment_fund = models.BooleanField(null=True, default=False)

    rta_scheme_planoptiondesc = models.CharField(max_length=100, blank=True, null=True)

    rta_stp_reg_in = models.CharField(max_length=10, null=True, blank=True)
    rta_stp_reg_out = models.CharField(max_length=10, null=True, blank=True)

    rta_scheme_name = models.CharField(max_length=500, null=True, blank=True) #desc of json

    rta_lock_in_period_flag = models.CharField(max_length=6, null=True, blank=True)
    rta_lock_in_period = models.CharField(max_length=15, null=True, blank=True)

    rta_scheme_type = models.CharField(max_length=25, null=True, blank=True)
    
    def __str__(self):
        return str(self.name)
    
    @classmethod
    def get_fund_obj(self, fund):
        fund_obj = AMCFund.objects.get(rta_fund_code=fund['scheme'])
        return fund_obj
    
    @classmethod
    def save_scheme(self, scheme, scheme_payload):
        try:
            if not AMCFundScheme.objects.filter(rta_scheme_code=scheme['schemeid']).exists(): 
                AMCFundScheme.objects.create(**scheme_payload)
            else:
                obj = AMCFundScheme.objects.get(rta_scheme_code=scheme['schemeid'])
                for key, val in scheme_payload.items():
                    setattr(obj, key, scheme[val])
                obj.save()

        except Exception as e:
            # print(f"Error encountered while saving scheme {scheme['schemeid']}: {e}")
            # print("Skipping this entry and moving to next one")
            pass

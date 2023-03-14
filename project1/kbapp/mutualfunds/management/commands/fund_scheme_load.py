from django.core.management.base import BaseCommand
import requests
from kbapp.models import AMCFund, AMCFundScheme
import datetime
import warnings
warnings.filterwarnings("ignore")


def get_data_from_api(url):
    response = requests.get(url)
    data = response.json()
    return data

def fund_payload():
    payload = {
        "rta_fund_code": "scheme",
        "name": "schdesc",
        "fund_type": "category",
        "fund_category": "category",
        "fund_sub_type": "subcategory",
        "risk_factor": "risktype",
    }
    return payload

def get_cutoff_time(param):
    str_time = str(param)
    if len(str_time) == 4:
            cutoff_time_hour = int(str_time[:2])
            cutoff_time_min = int(str_time[2:])
            cut_off_time = datetime.time(cutoff_time_hour, cutoff_time_min)
    else:
        cut_off_time = ''

    return cut_off_time

def load_scheme_payload(scheme, fund_obj):
    is_direct_fund = 'direct' if 'direct' in scheme['plandesc'] else False
    is_regular_fund = 'regular' if 'regular' in scheme['plandesc'] else False

    is_growth_fund = 'growth' if 'growth' in scheme['optiondesc'] else False
    is_div_payout_fund = 'payout' if 'payout' in scheme['optiondesc'] else False
    is_div_reinvestment_fund = 'reinvestment' if 'reinvestment' in scheme['optiondesc'] else False

    planoptiondesc = {
        is_direct_fund and is_growth_fund: "Direct & Growth",
        is_regular_fund and is_growth_fund: "Regular & Growth", 
        is_direct_fund and is_div_reinvestment_fund: "Direct & IDCW Reinvestment", 
        is_regular_fund and is_div_reinvestment_fund: "Regular & IDCW Reinvestment", 
        is_direct_fund and is_div_payout_fund: "Direct & IDCW Payout", 
        is_regular_fund and is_div_payout_fund: "Regular & IDCW Payout"
        }

    scheme_payload = {
        "AMCFund": fund_obj,
        "name": scheme['desc'],
        "amfi_scheme_code": scheme['amficode'] if scheme['amficode'] else 0,
        "is_active": True if scheme['active'] == "Y" else False,
        
        "is_being_sold": True if scheme['purallow'] == "Y" else False,
        "is_direct_fund": is_direct_fund,
        "is_regular_fund": is_regular_fund,
        "is_growth_fund": is_growth_fund,
        "is_div_payout_fund": is_div_payout_fund,
        "is_div_reinvestment_fund": is_div_reinvestment_fund,
        "rta_scheme_planoptiondesc": planoptiondesc.get(True, ""),
        "rta_scheme_option": scheme.get("optiondesc"),
        "rta_sip_flag": scheme['sipallow'],
        "rta_stp_flag": scheme['stpoallow'],
        "rta_swp_flag": scheme['stpiallow'],
        "rta_switch_flag": "Y" if scheme['swiallow'] == 'Y' and scheme['swoallow'] == 'Y' else "N",
        "rta_stp_reg_in": scheme['stpiallow'],
        "rta_stp_reg_out": scheme['stpoallow'],

        "rta_scheme_code": scheme['schemeid'],
        "rta_rta_scheme_code": scheme['schemeid'],
        "rta_amc_scheme_code": scheme['schemeid'],
        "rta_isin": scheme['isin'],
        "rta_amc_code": scheme['fundname'],
        "rta_scheme_type": fund_obj.fund_category,
        "rta_scheme_plan": scheme['plandesc'],
        "rta_scheme_name": scheme['desc'],
        "rta_scheme_active_flag": scheme['active'],
        "rta_lock_in_period_flag": "N",
        "rta_lock_in_period": 0,
        "rta_plan_code": scheme['plan'],
        "rta_option_code": scheme['option'],

        "is_nfo": scheme['nfoidentifier'],
        "nfo_face_value": scheme['facevalue'],
        "nfo_start_date": datetime.datetime.fromisoformat(scheme['opendate'][:-1] + '+00.00').date(), 
        "nfo_end_date": datetime.datetime.fromisoformat(scheme['closedate'][:-1] + '+00.00').date(), 
        "nfo_reopening_date": datetime.datetime.fromisoformat(scheme['reopendate'][:-1] + '+00.00').date(),  

        # Scheme Purchase Fields
        "rta_purchase_allowed": scheme['purallow'],
        "rta_minimum_purchase_amount": scheme['new_minamt'],
        "rta_additional_purchase_amount_multiple": scheme['add_minamt'],
        "rta_purchase_cutoff_time": get_cutoff_time(scheme['purcuttime']),  # Convert to datetime.time

        # Scheme Redeem Fields
        "rta_redemption_allowed": scheme['redallow'],
        "rta_redemption_amount_minimum": scheme['red_minamt'],
        "rta_redemption_cutoff_time": get_cutoff_time(scheme['redcuttime']),  # Convert to datetime.time
        "modified_by": 'Admin',
        "modified": datetime.datetime.now()
        }
    
    return scheme_payload

def store_fund_scheme_data(data):
    for fund in data['data']['funds']:
        fund_obj = AMCFund.get_fund_obj(fund['scheme'])

        for scheme in fund['schemes']:
            scheme_payload = load_scheme_payload(scheme, fund_obj)
            AMCFundScheme.save_scheme(scheme,scheme_payload)
                


class Command(BaseCommand):
    def handle(self, *args, **options):
        url = "https://clientwebsitesuat3.kfintech.com/bajaj/api/v1/masterData/getSchemes"
        data = get_data_from_api(url)
        payload_fund = fund_payload()
        AMCFund.store_fund_data(payload_fund, data)
        store_fund_scheme_data(data)

from django.core.management.base import BaseCommand
import requests
from kbapp.models import AMCFund
import datetime

# Our data coming from the api looks like this:
# {
# "statusCode": "0",
# "message": "success",
# "data": {
#     "fund": "189",
#     "fundname": "Bajaj MUTUAL FUND",
#     "funds": [
#         {
#             "scheme": "IS",
#             "schdesc": "Bajaj Regular Saver Fund",
#             "category": "DEBT FUND",
#             "subcategory": "DEBT",
#             "risktype": "MODERATELY HIGH",
#             "schemes":[....]
#         },
#         {
#             "scheme": "IS",

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

def store_fund_data(data):
    payload = fund_payload()
    for fund in data['data']['funds']:
        # print(f"{fund['scheme']} | {fund['schdesc']} | {fund['category']} | {fund['subcategory']} | {fund['risktype']}")
        obj = AMCFund.objects.filter(rta_fund_code=fund['scheme']).first()
        if obj:
            for key, value in payload.items():
                setattr(obj, key, fund[value])
            obj.modified_by = "Admin User"
            obj.modified = datetime.datetime.now()
            obj.save()
        else:
            obj_new = AMCFund(**payload)
            for key, value in payload.items():
                setattr(obj_new, key, fund[value])
            obj_new.created_by = "Admin User"
            obj_new.created = datetime.datetime.now()
            obj_new.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        url = "https://clientwebsitesuat3.kfintech.com/bajaj/api/v1/masterData/getSchemes"
        data = get_data_from_api(url)
        print(store_fund_data(data))

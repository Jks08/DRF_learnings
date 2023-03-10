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

# Now, we work on the schemes list.
# The schemes list contains data of all the scehemes.
# It looks like this:
# "schemes": [
#                     {
#                         "code": null,
#                         "fundname": "Bajaj MUTUAL FUND",
#                         "schemeid": "ISQDD",
#                         "scheme": "IS",
#                         "schdesc": "Bajaj Regular Saver Fund",
#                         "plan": "QD",
#                         "plandesc": "Regular Quarterly IDCW",
#                         "option": "D",
#                         "optiondesc": "Payout",
#                         "active": "Y",
#                         "execdt": "2010-07-16T00:00:00.000Z",
#                         "opendate": "2010-05-24T00:00:00.000Z",
#                         "nav_sp": 4,
#                         "desc": "Bajaj Regular Saver Fund Regular Quarterly IDCW Payout",
#                         "prodcode": "XS71",
#                         "nature": "Open",
#                         "closedate": "2010-06-21T00:00:00.000Z",
#                         "purcuttime": 1500,
#                         "redcuttime": 1500,
#                         "swicuttime": 1500,
#                         "maturitydt": "9999-03-06T00:00:00.000Z",
#                         "purallow": "Y",
#                         "redallow": "Y",
#                         "swiallow": "Y",
#                         "swoallow": "Y",
#                         "latiallow": "Y",
#                         "latoallow": "Y",
#                         "stpiallow": "Y",
#                         "stpoallow": "Y",
#                         "sipallow": "Y",
#                         "swdallow": "Y",
#                         "mcrid": "A3",
#                         "sweepinallow": "Y",
#                         "sweepoutallow": "Y",
#                         "allotmentdt": "2010-07-16T00:00:00.000Z",
#                         "isin": "INF846K01701",
#                         "shortdesc": "AXF REG SAVER FUND  DIVD(QLY)",
#                         "nfoallow": null,
#                         "facevalue": 10,
#                         "amficode": "112925",
#                         "reopendate": "2010-05-24T00:00:00.000Z",
#                         "nfoidentifier": "",
#                         "new_minamt": 5000,
#                         "add_minamt": null,
#                         "red_minamt": 0,
#                         "sip_minamt": null,
#                         "swp_minamt": 1000,
#                         "stp_minamt": 1000,
#                         "switch_minamt": 0
#                     },
#                     {

# and then other schemes.
# This goes on till the end of the list. After that we have the next fund. So, we need to iterate over the funds list and then the schemes list.


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

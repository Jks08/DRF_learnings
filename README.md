# DRF_Demo

Demo work on DRF

- [X] Customer can add only 4 account at max.
- [X] In GET bank API ; only active bank to be shown ; hence only ONE bank should come in GET Bank API response.
- [X] Maximum of 4 banks ( 3 inactive + 1 active) to be allowed per PAN.
- [X] Unique bank to be identified basis Unique combination of IFSC + Account Number
- [X] PUT method to be allowed to update/add new information. If verification status true, cannot update from API and send cannot update message ; else update.
- [X] Required Fields to create bank account {"customer", "name_as_per_bank_record", "ifsc_code", "account_number", "account_type", bank", "branch_name"}
- [X] Bank Logo should be fetch in response only.
- [X] One customer can have only one account in one bank

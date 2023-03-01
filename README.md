# DRF_Demo

The main project files and directories are in [project1](https://github.com/Jks08/DRF_learnings/tree/main/project1) directory

- [X] Customer can add only 4 account at max.
- [X] In GET bank API ; only active bank to be shown ; hence only ONE bank should come in GET Bank API response.
- [X] Maximum of 4 banks ( 3 inactive + 1 active) to be allowed per PAN.
- [X] Unique bank to be identified basis Unique combination of IFSC + Account Number
- [X] PUT method to be allowed to update/add new information. If verification status true, cannot update from API and send cannot update message ; else update.
- [X] Required Fields to create bank account {"customer", "name_as_per_bank_record", "ifsc_code", "account_number", "account_type", bank", "branch_name"}
- [X] Bank Logo should be fetch in response only.
- [X] One customer can have only one account in one bank

# Some Pointers to Note

- In the bankaccount/ POST, PUT and PATCH request all the fields are required in the JSON, but only the following get altered: ifsc_code, branch_name, name_as_per_bank_record and account_type.
- The input for the "customer" and "bank" field is of the data type integer (number), and their value can be got from the GET method for '/customerdata/customerdetail/'.
- Only to create a new customer can be donwe without authentication and rest all actions can only be done through authenticated users.

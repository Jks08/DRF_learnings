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
- [X] If data is sent to create a bank account via POST and it exactly matches data present in a bank account with is_active=False, make it the active bank account and deactivate others.

# Some Pointers to Note

- In the bankaccount/ POST, PUT and PATCH request all the fields are required in the JSON, but only the following get altered: ifsc_code, branch_name, name_as_per_bank_record and account_type.
- The input for the "customer" and "bank" field is of the data type integer (number), and their value can be got from the GET method for '/customerdata/customerdetail/'.
- Only to create a new customer can be donwe without authentication and rest all actions can only be done through authenticated users.

# Working of the Project

1. To create a new user, no authentication is required, and a POST request has to be made to http://127.0.0.1:8000/customerdata/customerdetail/ with the following JSON details:

   ```json
   {
       "email": "",
       "first_name": "",
       "last_name": "",
       "pan_no": "",
       "password": ""
   }

   ```
2. Bank Account for a user can only be created via POST, after Token verification. Token verification is done through: https://127.0.0.1:8000/api-token-auth/ and takes in the following JSON:

   ```JSON
   {
       "email": "",
       "password": ""
   }

   ```
3. After Token generation, pass it to Header.
4. To create new bank account, POST request to this url: http://127.0.0.1:8000/customerdata/bankaccount/ and in the following JSON format:

   ```json
   {
       "account_number": "0001",
       "ifsc_code": "tokyo",
       "customer": 16,
       "bank":1,
       "branch_name": "hiroshima",
       "name_as_per_bank_record": "test2",
       "account_type": "Current"
   }

   ```
5. GET method on this url http://127.0.0.1:8000/customerdata/bankaccount/ will output active bank account for authorized user.
7. PUT or PATCH on http://127.0.0.1:8000/customerdata/bankaccount/id will change the following details only: ifsc_code, branch_name, name_as_per_bank_record and account_type.

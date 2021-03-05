# zendesk_ticket_metrics

This repository contains a script to read ticket metrics from Zendesk API. 
It is currently filtered to only get metrics starting 01/12/2020, but can be easily adjusted.
The script gets all tickets created starting from 01/12/2020 to today. After that iterates on each ticket to get it's metrics.

Endpoints used:
/api/v2/tickets/
/api/v2/tickets/metrics

The script needs login information with following format:
zendesk_user = 'youremail@domain.com'
zendesk_pwd = yourencryptedpassword
encrypt_key = yourFernetkey

Since the script needs user's password to authenticate access, you will have to encrypt it using python's Fernet library:
from cryptography.fernet import Fernet

The encryption method has it's flaws, but at least prevents direct access to the user's password.


"""
export a csv of the current eratos active users.
"""

import os


import csv

from eratos.creds import AccessTokenCreds
from eratos.adapter import Adapter
from eratos.ern import Ern

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib
import ssl
import json

import smtplib, ssl
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
port = 465  # For SSL


sender_email = "eratos.email.service@gmail.com"
password = "LookILikeSheep!"
new_pword = "afdwmuerjetldqdb"
receiver_email = "kate@eratos.com"



creds_path = r"C:\Users\Quinten\Documents\Eratos_tok\mycreds.json"


# Opening JSON file
f = open(creds_path)
  
# returns JSON object as 
# a dictionary
creds = json.load(f)

ecreds = AccessTokenCreds(
  creds['key'],
  creds['secret']
)

adapter = Adapter(ecreds)

# Create a multipart message
msg = MIMEMultipart()
body_part = MIMEText("Here is the daily Eratos user export.", 'plain')
msg['Subject'] = "Current Eratos User List"
msg['From'] = sender_email
msg['To'] = receiver_email
# Add body to email
msg.attach(body_part)
# open and read the CSV file in binary
with open(export_path,'rb') as file:
# Attach the file with filename to the email
    msg.attach(MIMEApplication(file.read(), Name="EratosUserExport.csv"))

context = ssl.create_default_context()
# Create SMTP object

with smtplib.SMTP_SSL("smtp.gmail.com",port=port, context=context) as server:
        server.login(sender_email, new_pword)


        
        server.sendmail(sender_email, receiver_email, msg.as_string()
            )
print('done')
# try:
#     smtp_obj = smtplib.SMTP("smtp.gmail.com", port=587)
#     smtp_obj.ehlo()
#     # Login to the server
#     smtp_obj.starttls(context=context)
#     smtp_obj.ehlo()
#     smtp_obj.login(sender_email, password)

#     # Convert the message to a string and send it
#     smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
# except Exception as e:
#     # Print any error messages to stdout
#     print('error')
#     print(e)
# finally:
#     smtp_obj.quit()
    
# # print('Total Users: ',count)
# print('done')

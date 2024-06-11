import requests
from datetime import datetime, timedelta
import time
import pytz
from os import environ

Define all the constants
time_interval = 20  # (in seconds) Specify the frequency of code execution
PINCODE = "801503"
msg = "Blank"
tele_auth_token = environ['Tele_auth_tok'] # Authentication token provided by Telegram bot
tel_group_id = "Test_Telegram_group"      # Telegram group name
IST = pytz.timezone('Asia/Kolkata')           # Indian Standard Time - Timezone
slot_found =  False                                   # Intial slot found status
header = {'User-Agent': 'Chrome/84.0.4147.105 Safari/537.36'}
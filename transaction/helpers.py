import requests
import random
from django.conf import settings
from django.core.mail import send_mail
import os
from twilio.rest import Client
from django.conf import settings
account_sid = settings.ACCOUNT_SID
auth_token = settings.AUTH_TOKEN
verify_sid = settings.VERIFY_SID
def send_otp_to_phone(phone_number):
    try:
        otp = random.randint(1000, 9999)
        print("Sending the request")
        client = Client(account_sid, auth_token)
        print(phone_number)
        verification = client.verify.v2.services(verify_sid) \
        .verifications \
        .create(to=phone_number, channel="sms")
        print("Api calling",verification.status)
        return otp
    except Exception as e:
        return 0
    
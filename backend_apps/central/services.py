import requests
import json
import hashlib
import base64
from django.conf import settings
import time
import random
import time
import random

class PhonePeService:

    @staticmethod
    def get_base_url():
        """Get the PhonePe base URL based on the environment flag"""
        return settings.PHONEPE_PROD_URL if settings.PHONEPE_ENV == "PROD" else settings.PHONEPE_TESTING_URL

    @staticmethod
    def get_merchant_id():
        """Get the merchant ID based on the environment"""
        if settings.PHONEPE_ENV == "PROD":
            return settings.PHONEPE_PROD_MERCHANT_ID
        return settings.PHONEPE_TESTING_MERCHANT_ID

    @staticmethod
    def generate_merchant_transaction_id():
        """Generate a random 30-digit merchant transaction ID with epoch time"""
        epoch_time = int(time.time() * 1000)  # Current epoch time in milliseconds
        random_number = random.randint(10**(30 - len(str(epoch_time)) - 1), (10**(30 - len(str(epoch_time))) - 1))
        return f"{epoch_time}{random_number}"

    @staticmethod
    def generate_merchant_user_id():
        """Generate a random 30-digit merchant user ID with epoch time"""
        epoch_time = int(time.time() * 1000)  # Current epoch time in milliseconds
        random_number = random.randint(10**(30 - len(str(epoch_time)) - 1), (10**(30 - len(str(epoch_time))) - 1))
        return f"{epoch_time}{random_number}"

    @staticmethod
    def get_salt_key():
        """Get the salt key based on the environment"""
        if settings.PHONEPE_ENV == "PROD":
            return settings.PHONEPE_PROD_SALTKEY
        return settings.PHONEPE_TESTING_SALTKEY

    @staticmethod
    def get_salt_index():
        """Get the salt index based on the environment"""
        if settings.PHONEPE_ENV == "PROD":
            return settings.PHONEPE_PROD_SALTINDEX
        return settings.PHONEPE_TESTING_SALTINDEX

    @staticmethod
    def create_payload(amount, transaction_id, callback_url):
        """Generate the payload for PhonePe payment"""
        payload = {
            "merchantId": PhonePeService.get_merchant_id(),
            "transactionId": transaction_id,
            "amount": int(amount * 100),  # Convert amount to paise
            "callbackUrl": callback_url,
            "mobileNumber": "9999999999",
            "paymentInstrument": {
                "type": "PAY_PAGE"
            }
        }
        return json.dumps(payload)

    @staticmethod
    def generate_checksum(payload):
        """Generate the checksum for PhonePe request"""
        salt_key = PhonePeService.get_salt_key()
        data = payload + salt_key
        checksum = hashlib.sha256(data.encode()).hexdigest()
        return base64.b64encode(checksum.encode()).decode()
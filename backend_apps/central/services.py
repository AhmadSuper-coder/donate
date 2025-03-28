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
    def generate_payload_to_base64(payload):
        """
        Generate a Base64 encoded payload for PhonePe API.
        
        Args:
            payload (dict): The payload to be sent in the request.
        
        Returns:
            str: Base64 encoded payload.
        """
        
        # Convert payload to JSON string
        payload_json = json.dumps(payload)
        
        # Encode the JSON string to bytes
        payload_bytes = payload_json.encode('utf-8')
        
        # Encode the bytes to Base64
        base64_payload = base64.b64encode(payload_bytes).decode('utf-8')
        
        return base64_payload



    @staticmethod
    def create_request_body(payload):
        """
        Create the request body for PhonePe API.
        
        Args:
            payload (dict): The payload to be sent in the request.
        
        Returns:
            dict: A dictionary containing the request body.
        """
        # Convert payload to Base64
        base64_payload = PhonePeService.generate_payload_to_base64(payload)
        
        # Return the request body
        return {"request": base64_payload}



    @staticmethod
    def generate_request_headers(endpoint, payload):
        # Convert payload to Base64
        base64_payload = PhonePeService.generate_payload_to_base64(payload)

        # Calculate X-Verify Header
        salt_key = PhonePeService.get_salt_key()
        salt_index = PhonePeService.get_salt_index()
        checksum_data = f"{base64_payload}{endpoint}{salt_key}"
        x_verify = hashlib.sha256(checksum_data.encode()).hexdigest() + "###" + salt_index
        
        return {
            "Content-Type": "application/json",
            "X-VERIFY": x_verify
        }

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
    def generate_checksum(payload):
        """Generate the checksum for PhonePe request"""
        salt_key = PhonePeService.get_salt_key()
        data = payload + salt_key
        checksum = hashlib.sha256(data.encode()).hexdigest()
        return base64.b64encode(checksum.encode()).decode()


    # from here will be mention all the url for the payment 
    @staticmethod
    def one_time_payment_url():
        """Get the one-time payment URL for PhonePe"""
        return f"{PhonePeService.get_base_url()}/pg/v1/pay"


        

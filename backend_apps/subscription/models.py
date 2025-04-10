from django.db import models
import hashlib
from backend_apps.central.services import PhonePeService
from backend_apps.central import constants as PhonePeConstants
import requests  # Ensure requests is used for HTTP requests

# Create your models here.

class Subscription(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Success", "Success"),
    ]

    FREQUENCY_CHOICES = [
        ("Weekly", "Weekly"),
        ("Monthly", "Monthly"),
        ("Quarterly", "Quarterly"),
        ("Yearly", "Yearly"),
    ]

    SITE_CHOICES = [
        ("x.com", "x.com"),
        ("y.com", "y.com"),
    ]

    # site = models.CharField(max_length=10, choices=SITE_CHOICES, default="x.com")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mobile = models.CharField(max_length=255)  # Encrypted data
    name = models.CharField(max_length=255)  # Encrypted data
    pan = models.CharField(max_length=10, blank=True, null=True)  # Encrypted data
    email = models.EmailField()  # Encrypted data
    state = models.CharField(max_length=100)  # Encrypted data
    phonepe_subscription_id = models.CharField(max_length=255, null=True, blank=True)
    merchant_subscription_id = models.CharField(max_length=255, null=True, blank=True)
    merchant_user_id = models.CharField(max_length=255, null=True, blank=True)
    frequency = models.CharField(
        max_length=10, choices=FREQUENCY_CHOICES, blank=True, null=True
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")

    created_on = models.DateTimeField(auto_now_add=True)  # Set on creation
    updated_on = models.DateTimeField(auto_now=True)  # Updates on each save

    def __str__(self):
        return f"{self.name} - {self.amount}"


    def check_subscription_creation_status(merchant_id, merchant_subscription_id, api_endpoint):
        """
        Check the status of a subscription creation.
        Args:
            merchant_id (str): The merchant ID.
            merchant_subscription_id (str): The merchant subscription ID.
            api_endpoint (str): The API endpoint for checking status.
        
        Returns:
            bool: True if the subscription is successfully created, False otherwise.
        """

        full_api_endpoint = f"{api_endpoint}/{merchant_id}/{merchant_subscription_id}"
        headers = PhonePeService.generate_request_headers(full_api_endpoint)
        subscription_creation_url = PhonePeService.get_phonepe_url(full_api_endpoint)

        response = requests.get(subscription_creation_url, headers=headers, json={})

        if response.status_code == 200:
            response_data = response.json()
            if (
                response_data.get("success") is True
                and response_data.get("code") == "SUCCESS"
                and response_data.get("data", {}).get("state") == "CREATED"
            ):
                return True

        return False
    

    def submit_auth_request(api_endpoint, merchant_id, merchant_user_id, subscription_id, auth_request_id, amount, callback_url):
        """
        Submit an authorization request to the API.

        Args:
            api_endpoint (str): The API endpoint for submitting the auth request.
            merchant_id (str): The merchant ID.
            merchant_user_id (str): The merchant user ID.
            subscription_id (str): The subscription ID.
            auth_request_id (str): The authorization request ID.
            amount (int): The amount in smallest currency unit (e.g., paise for INR).

        Returns:
            dict: The response from the API.
        """
        payload = {
            "merchantId": merchant_id,
            "merchantUserId": merchant_user_id,
            "subscriptionId": subscription_id,
            "authRequestId": auth_request_id,
            "amount": amount,
            "paymentInstrument": {
                "type": "UPI_QR"
            }
        }


    
        headers = PhonePeService.generate_request_headers(payload, api_endpoint, callback_url=callback_url)
        auth_request_url = PhonePeService.get_phonepe_url(api_endpoint)
        request_body = PhonePeService.create_request_body(payload)

        response = requests.post(auth_request_url, headers=headers, json=request_body)
        print("*************************************************************************")
        print(headers)
        print(auth_request_url)
        print(payload)
        print(response)
        print(api_endpoint)
        print(request_body)
        print("*************************************************************************")
        if response.status_code == 200:
            response_data = response.json()
            print("Response Data For THe Auth api:", response_data)
            
            return response.json()
        else:
            print("Error in response:", response.status_code, response.text)
            return None

    def get_status_url(merchant_id, merchant_subscription_id):
        """
        Generate the URL for checking subscription status.

        Args:
            merchant_id (str): The merchant ID.
            merchant_subscription_id (str): The merchant subscription ID.

        Returns:
            str: The generated URL.
        """
        return f"https://api-preprod.phonepe.com/apis/pg-sandbox/v3/recurring/subscription/status/{merchant_id}/{merchant_subscription_id}"
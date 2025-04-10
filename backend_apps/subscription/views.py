from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend_apps.central.services import PhonePeService
from backend_apps.subscription.models import Subscription
from backend_apps.central import constants as PhonePeConstants
import requests  # Ensure requests is used for HTTP requests

# Create your views here.
class SubscriptionRestoreView(APIView):

    def get(self, request, *args, **kwargs):
        # Logic for restoring a subscription
        # Example: Retrieve subscription data from request and process it
        print("8888888888888888888888888888888888888888888")
        print(request.data)
        return Response({"message": "Subscription restored successfully"}, status=status.HTTP_200_OK)

        subscription_id = request.data.get('subscription_id')
        if not subscription_id:
            return Response({"error": "Subscription ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Perform restore operation (placeholder logic)
        restored = True  # Replace with actual restore logic
        
        if restored:
            return Response({"message": "Subscription restored successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to restore subscription"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class CreateSubscriptionStatusView(APIView):
    def get(self, request, *args, **kwargs):
        subscription_id = request.query_params.get('subscription_id')
        if not subscription_id:
            return Response({"error": "Subscription ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            subscription = Subscription.objects.get(merchant_subscription_id=subscription_id)
        except Subscription.DoesNotExist:
            return Response({"error": "Subscription not found"}, status=status.HTTP_404_NOT_FOUND)

        subscription_status = {
            "id": subscription.id,
            "amount": subscription.amount,
            "mobile": subscription.mobile,
            "name": subscription.name,
            "email": subscription.email,
            "pan": subscription.pan,
            "state": subscription.state,
            "frequency": subscription.frequency,
            "status": subscription.status,
            "created_at": subscription.created_at,
        }

        return Response({"subscription_status": subscription_status}, status=status.HTTP_200_OK)



class SubscriptionCreateView(APIView):
    def post(self, request, *args, **kwargs):
        # Logic for creating a subscription
        # subscription_data = request.data.get('subscription_data')
        # if not subscription_data:
        amount = request.POST.get('amount')
        mobile = request.POST.get('mobile')
        name = request.POST.get('name')
        email = request.POST.get('email')
        pan = request.POST.get('pan')
        state = request.POST.get('state')
        frequency = request.POST.get('subscriptionFrequency')
        recurring_count =request.POST.get('recurring_count')
        merchant_subscription_id= PhonePeService.generate_merchant_transaction_id()
        merchant_user_id= PhonePeService.generate_merchant_user_id()
        auth_request_id= PhonePeService.generate_auth_request_id()
        merchant_id = PhonePeService.get_merchant_id()

        # Create a subscription object (replace with actual model and fields)
        Subscription.objects.create(
            amount=amount,
            mobile=mobile,
            name=name,
            email=email,
            pan=pan,
            state=state,    
            frequency=frequency,
            merchant_subscription_id=merchant_subscription_id,
            merchant_user_id=merchant_user_id,
            status="Pending",  # Default status            
        )

        # Prepare the payload for the subscription creation flow on PhonePe
        payload = {
            "merchantId": merchant_id,
            "merchantSubscriptionId": merchant_subscription_id,
            "merchantUserId": merchant_user_id,
            "authWorkflowType": "TRANSACTION",  # PENNY_DROP or TRANSACTION
            "amountType": "FIXED",  # FIXED or VARIABLE
            "amount": int(amount) * 100,  # Convert to smallest currency unit (e.g., paise)
            "frequency": frequency.upper(),  # Ensure frequency is in uppercase
            "recurringCount": recurring_count,  # Replace with actual recurring count if dynamic
            "mobileNumber": mobile,
        }

        request_body = PhonePeService.create_request_body(payload)
        headers = PhonePeService.generate_request_headers(PhonePeConstants.subscription_creation, payload)
        subscription_creation_url = PhonePeService.get_phonepe_url(PhonePeConstants.subscription_creation)

        # Send the request to PhonePe
        response = requests.post(subscription_creation_url, headers=headers, json=request_body)
        response_data = response.json()
        print("Response from PhonePe:", response_data)

        # Check if the response indicates success
        if response_data.get("success") and response_data.get("code") == "SUCCESS":
            print("Payload for PhonePe subscription:", payload)
            
            phonpe_subscription_id = response_data["data"].get("subscriptionId")
            # Save the subscription ID and state to the Subscription model
            subscription = Subscription.objects.get(merchant_subscription_id=merchant_subscription_id)
            subscription.phonepe_subscription_id = phonpe_subscription_id
            subscription.save()

            # Check the subscription creation status using the provided function
            status_response = Subscription.check_subscription_creation_status(
                merchant_id=merchant_id,
                merchant_subscription_id=merchant_subscription_id,
                api_endpoint=PhonePeConstants.subscription_status
            )

            if status_response:
                callback_url = request.build_absolute_uri('/subscription/auth/callback/')
                Subscription.submit_auth_request(PhonePeConstants.auth_init, merchant_id, merchant_user_id, phonpe_subscription_id, auth_request_id, amount, callback_url)
            



            # Log the status response for debugging
            print("Subscription creation status response:", status_response)

            if status_response:
                return Response({"message": "Subscription created successfully after intimation", "data": response_data.get("data")}, status=status.HTTP_201_CREATED)


            # Update the subscription status in the database based on the response
            # if status_response.get("success") and status_response.get("code") == "SUCCESS":
            #     subscription.status = status_response["data"].get("status", "Unknown")
            #     subscription.save()
            # else:
            #     return Response({"error": "Failed to verify subscription status", "details": status_response}, status=status.HTTP_400_BAD_REQUEST)

            # if status_response.get("success") and status_response.get("code") == "SUCCESS":
            #     subscription.status = status_response["data"].get("status", "Unknown")
            #     subscription.save()
            # else:
            #     return Response({"error": "Failed to verify subscription status", "details": status_response}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Subscription created successfully", "data": response_data.get("data")}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Failed to create subscription", "details": response_data}, status=status.HTTP_400_BAD_REQUEST)
        



class PhonePeAuthRequestView(APIView):
    def post(self, request, *args, **kwargs):
        # Logic for handling PhonePe authentication request
        phonepe_data = request.data.get('phonepe_data')
        if not phonepe_data:
            return Response({"error": "PhonePe data is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Perform authentication operation (placeholder logic)
        authenticated = True  # Replace with actual authentication logic
        
        if authenticated:
            return Response({"message": "PhonePe authentication successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "PhonePe authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)
        



class SubscriptionAuthCallbackView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract callback data from the request
        callback_data = request.data
        if not callback_data:
            return Response({"error": "Callback data is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Log the callback data for debugging
        print("Received callback data:", callback_data)

        # Extract necessary fields from the callback data
        merchant_subscription_id = callback_data.get("merchantSubscriptionId")
        status_code = callback_data.get("statusCode")
        status_message = callback_data.get("statusMessage")

        if not merchant_subscription_id:
            return Response({"error": "Merchant Subscription ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the subscription object using the merchant_subscription_id
            subscription = Subscription.objects.get(merchant_subscription_id=merchant_subscription_id)
        except Subscription.DoesNotExist:
            return Response({"error": "Subscription not found"}, status=status.HTTP_404_NOT_FOUND)

        # Update the subscription status based on the callback data
        subscription.status = status_message
        subscription.save()

        # Log the updated subscription for debugging
        print("Updated subscription:", subscription)

        return Response({"message": "Callback processed successfully"}, status=status.HTTP_200_OK)
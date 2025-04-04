from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from backend_apps.central.services import PhonePeService
from backend_apps.subscription.models import Subscription

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
        merchant_subscription_id= PhonePeService.generate_merchant_transaction_id()
        merchant_user_id= PhonePeService.generate_merchant_user_id()

        print("amount", amount)
        print("mobile", mobile)
        print("name", name)
        print("email", email)
        print("pan", pan)
        print("state", state)
        print("frequency", frequency)
        print("merchant_txn_id", merchant_subscription_id)
        print("merchant_user_id", merchant_user_id)

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
            "merchantId": PhonePeService.get_merchant_id(),
            "merchantSubscriptionId": merchant_subscription_id,
            "merchantUserId": merchant_user_id,
            "authWorkflowType": "PENNY_DROP",  # PENNY_DROP or TRANSACTION
            "amountType": "FIXED",  # FIXED or VARIABLE
            "amount": int(amount) * 100,  # Convert to smallest currency unit (e.g., paise)
            "frequency": frequency.upper(),  # Ensure frequency is in uppercase
            "recurringCount": 12,  # Replace with actual recurring count if dynamic
            "mobileNumber": mobile,
            "deviceContext": {
                "phonePeVersionCode": 400922  # Only for ANDROID, replace if needed
            }
        }

        print("Payload for PhonePe subscription:", payload)

  
        return Response({"message": "Subscription created, restored, and authenticated successfully"}, status=status.HTTP_201_CREATED)
        



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
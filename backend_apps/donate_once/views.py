from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views import View
from django.shortcuts import render, redirect
from backend_apps.central.services import PhonePeService


class DonateOnceView(View):
    def get(self, request):
        # Render the donation form
            print("GET request received")
            print(f"{PhonePeService.get_base_url()}, {PhonePeService.get_merchant_id()}, {PhonePeService.get_salt_key()}, {PhonePeService.generate_merchant_transaction_id()}, {PhonePeService.generate_merchant_user_id()}")
            return JsonResponse({'message': 'this is damn cool'}, status=200)

    def post(self, request):
        try:
            amount = request.POST.get('amount')
            mobile = request.POST.get('mobile')
            name = request.POST.get('name')
            email = request.POST.get('email')
            pan = request.POST.get('pan')
            state = request.POST.get('state')

            request_packet = {
                "merchantId": PhonePeService.get_merchant_id(),
                "merchantTransactionId": PhonePeService.generate_merchant_transaction_id(),
                "merchantUserId": PhonePeService.generate_merchant_user_id(),
                "amount": int(amount) * 100,  # Assuming amount is in rupees, converting to paise
                "redirectUrl": "https://webhook.site/redirect-url",
                "redirectMode": "REDIRECT",
                "callbackUrl": "https://webhook.site/callback-url",
                "mobileNumber": mobile,
                "paymentInstrument": {
                    "type": "PAY_PAGE"
                }
            }
            

            # if not amount or not donor_name:
            #     return JsonResponse({'error': 'Invalid data'}, status=400)`

            # Process the donation logic here (e.g., save to database)
            print(amount, mobile, name, email, pan, state)
            return JsonResponse({'message': 'Donation successful'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views import View
from django.shortcuts import render, redirect
from backend_apps.central.services import PhonePeService
from backend_apps.donate_once.models import DonateOnce
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class DonateOnceView(View):
    def get(self, request):
        # Render the donation form
            print("GET request received")
            redirect_url = request.build_absolute_uri('/donate-once/redirect/receipt/')
            callback_url = request.build_absolute_uri('/donate-once/callback/status/')
            print(redirect_url, callback_url)
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

            # Create a new donation entry in the database with status as 'pending'
            donation = DonateOnce.objects.create(
                amount=amount,
                mobile=mobile,
                name=name,
                email=email,
                pan=pan,
                state=state,
                status='pending'  # Assuming 'status' is a field in the Donation model
            )
            # Prepare the request packet for PhonePe
            # Assuming you have a method to get the merchant ID and other details
            # Generate the request packet for PhonePe
            # Define the redirect URL dynamically based on your application's domain or logic

            redirect_url = request.build_absolute_uri('/donate-once/redirect/receipt/')
            callback_url = request.build_absolute_uri('/donate-once/callback/status/')


            request_packet = {
                "merchantId": PhonePeService.get_merchant_id(),
                "merchantTransactionId": PhonePeService.generate_merchant_transaction_id(),
                "merchantUserId": PhonePeService.generate_merchant_user_id(),
                "amount": int(amount) * 100,  # Assuming amount is in rupees, converting to paise
                "redirectUrl": redirect_url,
                "redirectMode": "REDIRECT",
                "callbackUrl": callback_url,
                "mobileNumber": mobile,
                "paymentInstrument": {
                    "type": "PAY_PAGE"
                }
            }
            # Convert the request packet to Base64
            request_body = PhonePeService.create_request_body(request_packet)
            headers = PhonePeService.generate_request_headers(endpoint, base64_payload)

            print(request_body)
            # Send the request to PhonePe
            # Assuming you have a method to send the request to PhonePe
            # response = PhonePeService.send_request_to_phonepe(base64_payload)
            # For demonstration, let's assume the response is successful
            # Simulate a successful response from PhonePe
            response = {
                "success": True,
                "transactionId": PhonePeService.generate_merchant_transaction_id()
            }
            if response.get('success'):         
                # Redirect to PhonePe payment page
                transaction_id = response.get('transactionId')
                return JsonResponse({
                    'redirectUrl': f"{PhonePeService.get_base_url()}/v1/pay",
                    'transactionId': transaction_id
                }, status=200)
            else:
                return JsonResponse({'error': 'Payment initiation failed'}, status=500)
        except KeyError as e:
            return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': f'Invalid value: {str(e)}'}, status=400)
        except TypeError as e:
            return JsonResponse({'error': f'Invalid type: {str(e)}'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
   
            if not amount or not donor_name:
                return JsonResponse({'error': 'Invalid data'}, status=400)

            # Process the donation logic here (e.g., save to database)
            print(amount, mobile, name, email, pan, state)
            return JsonResponse({'message': 'Donation successful'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)




class RedirectReceiptView(View):
    """
    Handles the redirect after the payment is processed.
    Displays the receipt.
    """
    def get(self, request, *args, **kwargs):
        status = request.GET.get('status', 'unknown')
        transaction_id = request.GET.get('transactionId', '')
        print("------------------->>>>>>>>>>>. Redirection Url is Comming ------------------------>>>>>>>>>>")
        
        # Render receipt with transaction details
        return render(request, 'donation/receipt.html', {
            'status': status,
            'transaction_id': transaction_id
        })


# Ensure CSRF exemption for the callback view
@method_decorator(csrf_exempt, name='dispatch')  # Exempt CSRF for callback
class CallbackStatusView(View):
    """
    Handles the callback from PhonePe and updates the donation status.
    """
    def post(self, request, *args, **kwargs):
        try:

            print("------------------->>>>>>>>>>> Callback Status Url is Comming ------------------------>>>>>>>>>>")
            print(request)
            data = json.loads(request.data)  # Parse JSON payload
            transaction_id = data.get('transactionId')
            status = data.get('status')

            # Update the donation status in the database
            donation = DonateOnce.objects.get(id=transaction_id)
            donation.status = status
            donation.save()

            return JsonResponse({'message': 'Callback processed successfully'}, status=200)

        except DonateOnce.DoesNotExist:
            return JsonResponse({'error': 'Donation not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views import View
from django.shortcuts import render, redirect
from backend_apps.central.services import PhonePeService
from backend_apps.donate_once.models import DonateOnce, DonateOnceLog
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from backend_apps.central import constants as PhonePeConstants
import requests  # Ensure requests is used for HTTP requests
from django.utils.timezone import now
import time
from datetime import timedelta



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
            merchant_txn_id= PhonePeService.generate_merchant_transaction_id()
            merchant_user_id= PhonePeService.generate_merchant_user_id()


            # Generate the redirect and callback URLs
            # These URLs should point to your application's endpoints that handle the response from PhonePe
            # and the callback from PhonePe.
            # Create a new donation entry in the database with status as 'pending'
            donation = DonateOnce.objects.create(
                amount=amount,
                mobile_number=mobile,
                name=name,
                email=email,
                pan_number=pan,
                state=state,
                status='pending',  # Assuming 'status' is a field in the Donation model
                merchant_transaction_id=merchant_txn_id,
                merchant_user_id=merchant_user_id
            )

            # Generate the redirect URL with the donation ID
            redirect_url = request.build_absolute_uri(f'/donate-once/redirect/receipt/{donation.id}')
            callback_url = request.build_absolute_uri('/donate-once/callback/status/')


            request_packet = {
                "merchantId": PhonePeService.get_merchant_id(),
                "merchantTransactionId": merchant_txn_id ,
                "merchantUserId":merchant_txn_id,
                "amount": int(amount) * 100,  # Assuming amount is in rupees, converting to paise
                "redirectUrl": redirect_url,
                "redirectMode": "REDIRECT",
                "callbackUrl": callback_url,
                "mobileNumber": mobile,
                "paymentInstrument": {
                    "type": "PAY_PAGE"
                }
            }


            # Generate the request body, headers and phonepe URL
            request_body = PhonePeService.create_request_body(request_packet)
            headers = PhonePeService.generate_request_headers(PhonePeConstants.ph_one_time_payment_end_point, request_packet)
            phonepe_url = PhonePeService.get_phonepe_url(PhonePeConstants.ph_one_time_payment_end_point)

            # print(f"Request Body: {request_body}")
            # print(f"Headers: {headers}")
            # print(f"PhonePe URL: {phonepe_url}")

            # Send the request to PhonePe
            response = requests.post(phonepe_url, headers=headers, json=request_body)

            # Check the response from PhonePe
            if response.status_code == 200:
                response_data = response.json()
                DonateOnceLog.create_or_update(
                    donate_once_id=donation.id,
                    field_name='donate_once_response',
                    data=response_data
                )
                if response_data.get('success'):
                    # Handle successful response
                    redirect_info = response_data.get('data', {}).get('instrumentResponse', {}).get('redirectInfo', {})
                    payment_url = redirect_info.get('url')
                    if payment_url:
                        return redirect(payment_url)
                    if payment_url:
                        return JsonResponse({'redirectUrl': payment_url}, status=200)
                    else:
                        return JsonResponse({'error': 'Redirect URL not found in response'}, status=500)
                else:
                    # Handle failure response
                    return JsonResponse({'error': 'Payment initiation failed', 'details': response_data}, status=500)
            else:
                response_data = response.json()
                DonateOnceLog.create_or_update(
                    donate_once_id=donation.id,
                    field_name='donate_once_response',
                    data=response_data
                )
                print(f"Error: {response.status_code}, Response: {response.text}")
                # Handle HTTP error response
                return JsonResponse({'error': 'Failed to connect to PhonePe', 'status_code': response.status_code}, status=500)
            

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
   
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)




class RedirectReceiptView(View):
    """
    Handles the redirect after the payment is processed.
    Displays the receipt.
    """
    def get(self, request, *args, **kwargs):
        try:
            donation_id = kwargs.get('id')
            merchant_id= PhonePeService.get_merchant_id()
            try:
                donation = DonateOnce.objects.get(id=donation_id)
                data = {
                "id": donation.id,
                "amount": donation.amount,
                "transaction_id": donation.merchant_transaction_id,
                "registered_on": donation.created_on,
                "name": donation.name,
                "state": donation.state
                }
                
            except DonateOnce.DoesNotExist:
                return JsonResponse({'error': 'Donation not found'}, status=404)
            

            # if callback is present then transaction is successfullsuccess
            if donation.call_back_status:
                return render(request, 'receipt.html', {"data": data})


            # Generate the PhonePe status endpoint    
            response = PhonePeService.check_transaction_status(
                merchant_id=merchant_id,
                donation= donation
            )

            if response.status_code == 200:
                response_data = response.json()
                DonateOnceLog.create_or_update(
                    donate_once_id=donation.id,
                    field_name='status_api_response',
                    data=response_data
                )
                if response_data.get('success') and response_data.get('code') == 'PAYMENT_SUCCESS':
                    return render(request, 'receipt.html', {"data": data})
                elif response_data.get('success') and response_data.get('code') == 'PAYMENT_PENDING':
                    
                    # Check status every 3 seconds for the next 30 seconds
                    for t in range(5):  # 5 iterations of 3 seconds each
                        status_response = PhonePeService.check_transaction_status(
                            merchant_id=merchant_id,
                            donation=donation
                        )
                
                        status_response_data = status_response.json()
                        print("status_response_data", status_response_data)
                        if status_response_data.get('success') and status_response_data.get('code') == 'PAYMENT_SUCCESS':
                            return render(request, 'receipt.html', {"data": data})
                        elif status_response_data.get('success') and status_response_data.get('code') == 'PAYMENT_FAILED':
                            break
                        time.sleep(3)
   
                else:
                    # If not success or pending, then payment is failed
                    cancel_response =PhonePeService.cancel_transaction(
                        merchant_id=merchant_id,
                        donation=donation
                    )

                    cancel_response_data = cancel_response.json()
                    DonateOnceLog.create_or_update(
                    donate_once_id=donation.id,
                    field_name='cancelation_api_response',
                    data=cancel_response_data
                    )
                    if cancel_response_data.get('code') == 'PAYMENT_ALREADY_COMPLETED':
                        return render(request, 'receipt.html', {"data": data})
                    else:
                        return render(request, 'payment_failed.html', {"data": data})
            else:
                # logging the error response
                response_data = response.json()
                DonateOnceLog.create_or_update(
                    donate_once_id=donation.id,
                    field_name='status_api_response',
                    data=response_data
                )

                cancel_response = PhonePeService.cancel_transaction(
                    merchant_id=merchant_id,
                    donation=donation
                )

                cancel_response_data = cancel_response.json()
                DonateOnceLog.create_or_update(
                    donate_once_id=donation.id,
                    field_name='cancelation_api_response',
                    data=cancel_response_data
                )

                if cancel_response_data.get('code') == 'PAYMENT_ALREADY_COMPLETED':
                    return render(request, 'receipt.html', {"data": data})
                else:
                    return render(request, 'payment_failed.html', {"data": data})


            
            cancel_response = PhonePeService.cancel_transaction(
                merchant_id=merchant_id,
                donation=donation
            )

            cancel_response_data = cancel_response.json()
            DonateOnceLog.create_or_update(
                    donate_once_id=donation.id,
                    field_name='cancelation_api_response',
                    data=cancel_response_data
                )

            if cancel_response_data.get('code') == 'PAYMENT_ALREADY_COMPLETED':
                return render(request, 'receipt.html', {"data": data})
            else:
                return render(request, 'payment_failed.html', {"data": data})
                
    
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
        



# Ensure CSRF exemption for the callback view
@method_decorator(csrf_exempt, name='dispatch')  # Exempt CSRF for callback
class CallbackCancelsView(View):
    """
    Handles the callback from PhonePe and updates the donation status.
    """
    def post(self, request, *args, **kwargs):
        try:

            print("------------------->>>>>>>>>>> Callback Cancelation Url is Comming ------------------------>>>>>>>>>>")
            print(request)
            data = json.loads(request.data)  # Parse JSON payload
        

            return JsonResponse({'message': 'Callback processed successfully'}, status=200)

        except DonateOnce.DoesNotExist:
            return JsonResponse({'error': 'Donation not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
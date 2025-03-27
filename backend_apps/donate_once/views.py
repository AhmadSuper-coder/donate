from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views import View
from django.shortcuts import render, redirect

class DonateOnceView(View):
    def get(self, request):
        # Render the donation form
            return JsonResponse({'message': 'this is damn cool'}, status=200)

    def post(self, request):
        try:
            amount = request.POST.get('amount')
            mobile = request.POST.get('mobile')
            name = request.POST.get('name')
            email = request.POST.get('email')
            pan = request.POST.get('pan')
            state = request.POST.get('state')


            # if not amount or not donor_name:
            #     return JsonResponse({'error': 'Invalid data'}, status=400)\`/

            # Process the donation logic here (e.g., save to database)
            print(amount, mobile, name, email, pan, state)
            return JsonResponse({'message': 'Donation successful'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
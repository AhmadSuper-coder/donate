from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def home(request):
    return render(request, 'home.html', {"recurring_range": range(1, 16)})


def microservice_view(request):
    return render(request, 'policies.html')

from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')


def microservice_view(request):
    data = {"message": "Microservice is working!"}
    return JsonResponse(data)
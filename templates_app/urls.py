from django.urls import path
from .views import home, microservice_view

urlpatterns = [
    path('donate/ngo/', home, name='home'),
    path('', microservice_view, name='microservice_view'),
]

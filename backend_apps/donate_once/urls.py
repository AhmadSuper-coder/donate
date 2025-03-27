from django.urls import path
from . import views
from .views import DonateOnceView

urlpatterns = [
    path('api/donate/', DonateOnceView.as_view(), name='donate'),
]
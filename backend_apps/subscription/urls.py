from django.urls import path
from . import views
from .views import SubscriptionRestoreView

urlpatterns = [
    path('subscription/', SubscriptionRestoreView.as_view(), name='subscription_restore'),
    path('create/', views.SubscriptionCreateView.as_view(), name='subscription_create'),
]
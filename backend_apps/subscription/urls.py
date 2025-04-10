from django.urls import path
from . import views
from .views import SubscriptionRestoreView

urlpatterns = [
    path('subscription/', SubscriptionRestoreView.as_view(), name='subscription_restore'),
    path('create/', views.SubscriptionCreateView.as_view(), name='subscription_create'),
    path('auth-request/', views.PhonePeAuthRequestView.as_view(), name='phonepe_auth_request'),
    path('create/status/', views.CreateSubscriptionStatusView.as_view(), name='subscription_status'),
    path('auth/callback/', views.SubscriptionAuthCallbackView.as_view(), name='subscription_callback'),
]
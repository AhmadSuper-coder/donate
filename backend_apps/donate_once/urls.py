from django.urls import path
from . import views
from .views import DonateOnceView

urlpatterns = [
    path('donate-once/donate/', DonateOnceView.as_view(), name='donate'),
    path('donate-once/redirect/receipt/<int:id>/', views.RedirectReceiptView.as_view(), name='redirect_receipt'),
    path('donate-once/callback/status/', views.CallbackStatusView.as_view(), name='callback_status'),
    path('donate-once/callback/cancel/', views.CallbackCancelsView.as_view(), name='callback_cancels'),
]

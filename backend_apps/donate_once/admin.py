from django.contrib import admin
from .models import DonateOnce
from .models import DonateOnceLog

# Register your models here.

@admin.register(DonateOnce)
class DonateOnceAdmin(admin.ModelAdmin):
    list_display = ("id","name", "email", "mobile_number","merchant_transaction_id","merchant_user_id", "amount", "state", "status", "created_on", "updated_on")
    list_filter = ("status", "state", "created_on")
    search_fields = ("name", "email", "mobile_number", "pan_number")
    ordering = ("-created_on",)


@admin.register(DonateOnceLog)
class DonateOnceLogAdmin(admin.ModelAdmin):
    list_display = ("donate_once", "donate_once_response", "callback_response","status_api_response","cancelation_api_response")
    search_fields = ("donate_once", "id")
    ordering = ("-created_on",)


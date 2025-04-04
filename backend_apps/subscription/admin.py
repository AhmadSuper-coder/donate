from django.contrib import admin
from .models import Subscription

# Register your models here.

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "amount","merchant_subscription_id", "merchant_user_id",
        "frequency", "status","created_on", "updated_on"
    )
    list_filter = ("status", "frequency", "created_on")
    search_fields = ("name", "email", "mobile")
    ordering = ("-created_on",)

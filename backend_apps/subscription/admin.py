from django.contrib import admin
from .models import Subscription

# Register your models here.

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "name", "amount", "transaction_id",
        "frequency", "status", "site", "created_on", "updated_on"
    )
    list_filter = ("status", "frequency", "site", "created_on")
    search_fields = ("name", "email", "transaction_id", "mobile")
    ordering = ("-created_on",)

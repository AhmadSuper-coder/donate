from django.contrib import admin
from .models import DonateOnce

# Register your models here.

@admin.register(DonateOnce)
class DonateOnceAdmin(admin.ModelAdmin):
    list_display = ("id","name", "email", "mobile_number", "amount", "state", "status", "created_on", "updated_on")
    list_filter = ("status", "state", "created_on")
    search_fields = ("name", "email", "mobile_number", "pan_number")
    ordering = ("-created_on",)

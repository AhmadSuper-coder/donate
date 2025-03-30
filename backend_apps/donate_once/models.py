from django.db import models

# Create your models here.
class DonateOnce(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Success", "Success"),
        ("Failed", "Failed"),
    ]

    SITE_CHOICES = [
        ("x.com", "x.com"),
        ("y.com", "y.com"),
    ]


    site = models.CharField(max_length=10, choices=SITE_CHOICES, default="x.com")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mobile_number = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    pan_number = models.CharField(max_length=10, blank=True, null=True)
    state = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    merchant_transaction_id = models.CharField(max_length=255, blank=True, null=True)
    merchant_user_id = models.CharField(max_length=255, blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Set on creation
    updated_on = models.DateTimeField(auto_now=True)  # Updates on each save


    def __str__(self):
        return f"{self.name} - {self.amount} - {self.status}"
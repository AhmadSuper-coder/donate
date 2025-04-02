from django.db import models

# Create your models here.

class Subscription(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Success", "Success"),
    ]

    FREQUENCY_CHOICES = [
        ("Weekly", "Weekly"),
        ("Monthly", "Monthly"),
        ("Quarterly", "Quarterly"),
        ("Yearly", "Yearly"),
    ]

    SITE_CHOICES = [
        ("x.com", "x.com"),
        ("y.com", "y.com"),
    ]

    # site = models.CharField(max_length=10, choices=SITE_CHOICES, default="x.com")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mobile = models.CharField(max_length=255)  # Encrypted data
    name = models.CharField(max_length=255)  # Encrypted data
    pan = models.CharField(max_length=10, blank=True, null=True)  # Encrypted data
    email = models.EmailField()  # Encrypted data
    state = models.CharField(max_length=100)  # Encrypted data
    transaction_id = models.CharField(max_length=255, unique=True)
    frequency = models.CharField(
        max_length=10, choices=FREQUENCY_CHOICES, blank=True, null=True
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    upi_id = models.CharField(max_length=255, blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)  # Set on creation
    updated_on = models.DateTimeField(auto_now=True)  # Updates on each save

    def __str__(self):
        return f"{self.name} - {self.amount} - {self.transaction_id} - {self.site}"

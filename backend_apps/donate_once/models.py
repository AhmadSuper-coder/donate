from django.db import models

# Create your models here.
class DonateOnce(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]

    # SITE_CHOICES = [
    #     ("x.com", "x.com"),
    #     ("y.com", "y.com"),
    # ]


    # site = models.CharField(max_length=10, choices=SITE_CHOICES, default="x.com")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mobile_number = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    pan_number = models.CharField(max_length=10, blank=True, null=True)
    state = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    merchant_transaction_id = models.CharField(max_length=255, blank=True, null=True)
    merchant_user_id = models.CharField(max_length=255, blank=True, null=True)
    call_back_status = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Set on creation
    updated_on = models.DateTimeField(auto_now=True)  # Updates on each save


    def __str__(self):
        return f"{self.name} - {self.amount} - {self.status}"
    



class DonateOnceLog(models.Model):
    """
    Model to store logs of payment responses.
    """
    donate_once = models.ForeignKey(DonateOnce, on_delete=models.CASCADE, related_name="logs", null=True, blank=True)
    donate_once_response = models.JSONField(default=dict)
    callback_response = models.JSONField(default=dict)
    status_api_response = models.JSONField(default=dict)
    cancelation_api_response = models.JSONField(default=dict)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)

    @staticmethod
    def create_or_update(donate_once_id, field_name, data):
        """
        Creates a new log if it doesn't exist or updates an existing log.
        - Appends to the specified JSON field.

        :param donate_once_id: ID of the `DonateOnce` object
        :param field_name: Field to append data to
        :param data: New data to append (dict)
        """
        valid_fields = [
            'donate_once_response',
            'callback_response',
            'status_api_response',
            'cancelation_api_response'
        ]

        if field_name not in valid_fields:
            raise ValueError(f"Invalid field name: {field_name}")

        log, created = DonateOnceLog.objects.get_or_create(
            donate_once_id=donate_once_id,
            defaults={field_name: data}
        )

        if not created:
            # If the log exists, append/update the field data
            field_data = getattr(log, field_name, {})
            
            # Ensure the field is a dictionary
            if isinstance(field_data, dict):
                field_data.update(data)  # Append new data
                setattr(log, field_name, field_data)
                log.save()
                print(f"Log {log.id} updated successfully.")
            else:
                raise ValueError(f"The field {field_name} is not a dictionary.")
        else:
            print(f"New log created with ID: {log.id}")

        return log
    



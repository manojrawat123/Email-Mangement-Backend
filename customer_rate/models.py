from django.db import models
from customer.models import Customer
from django.utils import timezone
from management_profile.models import ManagementProfileName

class CustomerRateTable(models.Model):
    rate_name = models.CharField(max_length=255, unique=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customer_prefix = models.CharField(max_length=200, unique=True)
    rate_profile = models.ForeignKey(ManagementProfileName, on_delete=models.CASCADE)
    created_date = models.DateField(default=timezone.now)
    rate_status = models.CharField(max_length=20)
    def __str__(self):
        return self.rate_name
    
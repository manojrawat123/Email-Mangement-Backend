from django.db import models
from companycustomer.models import Customer
from django.utils import timezone
from management_profile.models import ManagementProfileName
from myusersession.models import CompanyUser

class CustomerRateTable(models.Model):
    rate_name = models.CharField(max_length=255)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    company_id = models.ForeignKey(CompanyUser, on_delete = models.CASCADE,limit_choices_to={'company_admin': True})
    customer_prefix = models.CharField(max_length=200)
    rate_profile = models.ForeignKey(ManagementProfileName, on_delete=models.CASCADE)
    created_date = models.DateField(default=timezone.now)
    rate_status = models.CharField(max_length=20)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company_id', 'rate_name'], name='unique_user_rate'),
            models.UniqueConstraint(fields=['company_id', 'customer_prefix'], name='unique_user_customer_prefix')
        ]
    def __str__(self):
        return self.rate_name
    
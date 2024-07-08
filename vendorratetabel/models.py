from django.db import models
from myusersession.models import CompanyUser
from companycustomer.models import Customer
from management_profile.models import ManagementProfileName

# Create your models here.
class VendorRateTabel(models.Model):
    company_id = models.ForeignKey(CompanyUser, on_delete=models.CASCADE,limit_choices_to={'company_admin': True})
    vendor_rate_name = models.CharField(max_length=200, unique=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vendor_prefix = models.CharField(max_length=200, unique=True)
    vendor_rate_profile = models.ForeignKey(ManagementProfileName, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now = True)
    rate_status = models.BooleanField(default = True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company_id', 'vendor_rate_name'], name='unique_vendor_rate'),
            models.UniqueConstraint(fields=['company_id', 'vendor_prefix'], name='unique_vendor_customer_prefix')
        ]

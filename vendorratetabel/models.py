from django.db import models
from myusersession.models import CompanyUser
from companycustomer.models import Customer
from management_profile.models import ManagementProfileName

# Create your models here.
class VendorRateTabel(models.Model):
    user_id = models.ForeignKey(CompanyUser, on_delete=models.CASCADE)
    vendor_rate_name = models.CharField(max_length=200, unique=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vendor_prefix = models.CharField(max_length=200, unique=True)
    vendor_rate_profile = models.ForeignKey(ManagementProfileName, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now = True)
    rate_status = models.BooleanField(default = True)

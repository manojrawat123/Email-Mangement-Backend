
from django.db import models
from myusersession.models import CompanyUser
from companycustomer.models import Customer
from management_profile.models import ManagementProfileName
from vendorratetabel.models import VendorRateTabel
from django.utils import timezone


# Create your models here.
class VendorRate(models.Model):
    company_id = models.ForeignKey(CompanyUser, on_delete=models.CASCADE,limit_choices_to={'company_admin': True})
    vendor_rate_id = models.ForeignKey(VendorRateTabel, on_delete=models.CASCADE)
    country_code = models.CharField(max_length=100)
    country_name = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    billing_increment_1 = models.IntegerField()
    billing_increment_n = models.IntegerField()
    status = models.CharField(max_length=20, default="active")  
    effective_date = models.DateField()
    created_date = models.DateField(default=timezone.now)
    rate_status = models.CharField(max_length=20)
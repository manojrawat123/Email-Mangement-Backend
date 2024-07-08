from django.db import models
from django.utils import timezone
from customer_rate.models import CustomerRateTable
from myusersession.models import CompanyUser

class RateTabel(models.Model):
    country_code = models.CharField(max_length=100)
    country_name = models.CharField(max_length=255)
    customer_rate_id = models.ForeignKey(CustomerRateTable, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    company_id = models.ForeignKey(CompanyUser, on_delete = models.CASCADE,limit_choices_to={'company_admin': True})
    billing_increment_1 = models.IntegerField()
    billing_increment_n = models.IntegerField()
    status = models.CharField(max_length=20, default="active")  
    effective_date = models.DateField()
    created_date = models.DateField(default=timezone.now)
    rate_status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.country_code} - {self.country_name}"

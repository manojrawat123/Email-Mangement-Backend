from django.db import models
from myusersession.models import CompanyUser
from countrycode.models import NewCountryCode

class Customer(models.Model):
    customer_name = models.CharField(max_length=100)
    company_id = models.ForeignKey(CompanyUser, on_delete = models.CASCADE, related_name="company",limit_choices_to={'company_admin': True})
    user_id = models.ForeignKey(CompanyUser, on_delete = models.CASCADE, related_name="user")
    # company_name = models.CharField(max_length=100)
    company_phone = models.CharField(max_length=15)
    rates_email = models.EmailField()
    billing_email = models.EmailField()
    country_code = models.ForeignKey(NewCountryCode, on_delete=models.CASCADE,related_name='customers_country_code')
    legal_email = models.EmailField()
    manager_name = models.CharField(max_length=100)
    created_date = models.DateField(auto_now_add=True)
    manager_email = models.EmailField()
    manager_phone_country_code = models.ForeignKey(NewCountryCode, on_delete=models.CASCADE,                                    related_name='customers_manager_phone_country_code')
    manager_phone = models.CharField(max_length=15)
    status = models.CharField(max_length=10, default='Active')
    active = models.BooleanField(default=True)
    dnd = models.BooleanField(default=False)
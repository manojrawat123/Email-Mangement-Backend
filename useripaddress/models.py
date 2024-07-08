from django.db import models
from myusersession.models import CompanyUser
from companycustomer.models import Customer


class IpAdderessCompanyCustomer(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    company_id = models.ForeignKey(CompanyUser, on_delete=models.CASCADE,limit_choices_to={'company_admin': True})
    active = models.BooleanField(default=True)
    added_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company_id', 'ip_address'], name='unique_ip_addresses'),
        ]

    def __str__(self):
        return f'Customer {self.customer_id} added by {self.added_by}'

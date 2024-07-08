from django.db import models
from companycustomer.models import Customer
from myusersession.models import CompanyUser


# Invoice Model

class Invoice(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)  
    company_id = models.ForeignKey(CompanyUser, on_delete = models.CASCADE,limit_choices_to={'company_admin': True})
    invoice_type = models.CharField(max_length=3, choices=[('IN', 'In'), ('OUT', 'Out')])
    invoice_number = models.CharField(max_length=200)
    invoice_from_date = models.DateField()
    invoice_to_date = models.DateField()
    invoice_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    invoice_minutes = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company_id', 'invoice_number'], name='unique_user_invoice')
        ]

    def __str__(self):
        return f'{self.invoice_number} - {self.customer_id}'
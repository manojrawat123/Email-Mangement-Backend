from django.db import models
from companycustomer.models import Customer
from invoice.models import Invoice
from myusersession.models import CompanyUser


# Create your models here.
class Dispute(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dispute_type = models.CharField(max_length=3, choices=[('IN', 'In'), ('OUT', 'Out')])
    company_id = models.ForeignKey(CompanyUser, on_delete = models.CASCADE,limit_choices_to={'company_admin': True})
    invoice_number = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    dispute_number = models.CharField(max_length=20)
    dispute_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    desc = models.TextField()
    active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company_id', 'dispute_number'], name='unique_user_dispute')
        ]
    def __str__(self):
        return f'{self.dispute_number} - {self.customer_id}'

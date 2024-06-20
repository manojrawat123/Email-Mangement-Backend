from django.db import models
from customer.models import Customer
from invoice.models import Invoice


# Create your models here.
class Dispute(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dispute_type = models.CharField(max_length=3, choices=[('IN', 'In'), ('OUT', 'Out')])
    invoice_number = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    dispute_number = models.CharField(max_length=20, unique = True)
    dispute_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    desc = models.TextField()
    active = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.dispute_number} - {self.customer_id}'

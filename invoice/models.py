from django.db import models
from customer.models import Customer


# Invoice Model
class Invoice(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    invoice_type = models.CharField(max_length=3, choices=[('IN', 'In'), ('OUT', 'Out')])
    invoice_number = models.CharField(max_length=20, unique = True)
    invoice_from_date = models.DateField()
    invoice_to_date = models.DateField()
    invoice_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.invoice_number} - {self.customer_id}'
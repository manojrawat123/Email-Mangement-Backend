from django.db import models
from customer.models import Customer

class Payment(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=50, choices=[('IN', 'In'), ('OUT', 'Out')])
    payment_date = models.DateField()
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bank_charges = models.DecimalField(max_digits=10, decimal_places=2)
    other_charges = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    payment_mode = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return f"Payment {self.id} - {self.payment_type}"


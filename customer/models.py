from django.db import models

class Customer(models.Model):
    customer_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    company_phone = models.CharField(max_length=15)
    rates_email = models.EmailField()
    billing_email = models.EmailField()
    legal_email = models.EmailField()
    manager_name = models.CharField(max_length=100)
    manager_email = models.EmailField()
    manager_phone = models.CharField(max_length=15)
    status = models.CharField(max_length=10, default='Active')
    active = models.BooleanField(default=True)
    dnd = models.BooleanField(default=False)


from django.db import models
from django.utils import timezone
from myusersession.models import CompanyUser

class Route(models.Model):
    top_route_name = models.CharField(max_length=255)
    date = models.DateField( default=timezone.now)  
    destination = models.CharField(max_length=255)
    profile = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=10, decimal_places=10) 
    asr = models.CharField(max_length=50) 
    user_id = models.ForeignKey(CompanyUser, on_delete = models.CASCADE, default=2)
    acd = models.CharField(max_length=50)   
    increment = models.CharField(max_length=50)  
    status = models.BooleanField(default=True) 
    def __str__(self):
        return self.top_route_name
    

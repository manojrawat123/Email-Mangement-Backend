from django.db import models
from django.utils import timezone

class Route(models.Model):
    top_route_name = models.CharField(max_length=255)
    date = models.DateField( default=timezone.now)  
    destination = models.CharField(max_length=255)
    profile = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=10, decimal_places=10) 
    asr = models.CharField(max_length=50) 
    acd = models.CharField(max_length=50)   
    increment = models.CharField(max_length=50)  
    status = models.BooleanField(default=True) 
    def __str__(self):
        return self.top_route_name
    

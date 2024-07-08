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
    company_id = models.ForeignKey(CompanyUser, on_delete = models.CASCADE, related_name="route_company_id",limit_choices_to={'company_admin': True})
    user_id = models.ForeignKey(CompanyUser, on_delete = models.CASCADE, related_name="route_user_id")
    acd = models.CharField(max_length=50)   
    increment = models.CharField(max_length=50)  
    status = models.BooleanField(default=True) 
    def __str__(self):
        return self.top_route_name
    

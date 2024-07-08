from django.db import models
from myusersession.models import CompanyUser

# Create your models here.
class ManagementProfileName(models.Model):
    
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)
    company_id = models.ForeignKey(CompanyUser, on_delete = models.CASCADE, limit_choices_to={'company_admin': True})

    def __str__(self):
        return self.name
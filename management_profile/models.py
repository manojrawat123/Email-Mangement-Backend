from django.db import models
from myusersession.models import CompanyUser

# Create your models here.
class ManagementProfileName(models.Model):
    
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)
    user_id = models.ForeignKey(CompanyUser, on_delete = models.CASCADE)

    def __str__(self):
        return self.name
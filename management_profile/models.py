from django.db import models

# Create your models here.
class ManagementProfileName(models.Model):
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.name
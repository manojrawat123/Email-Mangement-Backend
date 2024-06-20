from django.db import models

class Country(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
from django.db import models

# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=50, unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
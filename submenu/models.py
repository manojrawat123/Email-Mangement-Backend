from django.db import models
from menu.models import Menu

# Create your models here.
class Submenu(models.Model):
    label = models.CharField(max_length=50, unique=True)
    link = models.CharField(max_length=1000, unique=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
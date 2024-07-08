from django.db import models
from myusersession.models import CompanyUser
from menu.models import Menu
from submenu.models import Submenu


# Create your models here.
class MenuAccess(models.Model):
    user_id = models.OneToOneField(CompanyUser , on_delete= models.CASCADE)
    menu_id = models.ManyToManyField(Menu)
    company_id = models.ForeignKey(CompanyUser,on_delete=models.CASCADE, limit_choices_to={'company_admin': True}, related_name="company_id_menu_access")
    sub_menu = models.ManyToManyField(Submenu)
    active = models.BooleanField(default=True)
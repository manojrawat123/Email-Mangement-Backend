from django.db import models
from companycustomer.models import Customer
from emailtemplate.models import  EmailTemplate  
from django.utils import timezone
from django.core.exceptions import ValidationError
from myusersession.models import CompanyUser

class EmailRouteSchedule(models.Model):
    schedule_date_time = models.DateTimeField()
    company_id = models.ForeignKey(CompanyUser, on_delete = models.CASCADE, limit_choices_to={'company_admin': True})
    schedule_customer = models.ManyToManyField(Customer)
    schedule_template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE)
    schedule_route_id = models.CharField(max_length=250)
    status = models.CharField(max_length=250 , choices=(
        ('schedule', 'Schedule'),
        ('sent', "Sent"),
       
    ), default = 'schedule')
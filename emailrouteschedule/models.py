from django.db import models
from customer.models import Customer
from emailtemplate.models import  EmailTemplate  
from django.utils import timezone
from django.core.exceptions import ValidationError

class EmailRouteSchedule(models.Model):
    schedule_date_time = models.DateTimeField()
    schedule_customer = models.ManyToManyField(Customer)
    schedule_template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE)
    schedule_route_id = models.CharField(max_length=250)
    status = models.CharField(max_length=250 , choices=(
        ('schedule', 'Schedule'),
        ('sent', "Sent"),
       
    ), default = 'schedule')

    # def clean(self):
    #     if self.schedule_date_time <= timezone.now():
    #         raise ValidationError('The scheduled date and time must be in the future.')
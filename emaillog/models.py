from django.db import models
from companycustomer.models import Customer  # Import the Customer model from your app
from emailtemplate.models import EmailTemplate  # Import the EmailTemplate model from your app
from myusersession.models import CompanyUser

class EmailLog(models.Model):
    log_id = models.AutoField(primary_key=True)    
    company_id = models.ForeignKey(CompanyUser, on_delete = models.CASCADE,limit_choices_to={'company_admin': True})
    date = models.DateTimeField(auto_now_add=True)
    template_id = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE)
    customer_id = models.ManyToManyField(Customer)
    attachement = models.FileField(upload_to='email_attachments/', blank=True, null=True)

    def __str__(self):
        return f'Email Log ID: {self.log_id}'
  
from django.db import models
from customer.models import Customer  # Import the Customer model from your app
from emailtemplate.models import EmailTemplate  # Import the EmailTemplate model from your app

class EmailLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    template_id = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE)
    customer_id = models.ManyToManyField(Customer)
    attachement = models.FileField(upload_to='email_attachments/', blank=True, null=True)

    def __str__(self):
        return f'Email Log ID: {self.log_id}'
  
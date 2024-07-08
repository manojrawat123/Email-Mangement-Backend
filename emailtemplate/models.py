from myusersession.models import CompanyUser
from django.db import models

class EmailTemplate(models.Model):
    TemplateID = models.AutoField(primary_key = True)
    TemplateName = models.CharField(max_length = 100)
    TemplateSubject = models.CharField(max_length = 255)
    company_id = models.ForeignKey(CompanyUser, on_delete = models.CASCADE,limit_choices_to={'company_admin': True})
    template_body_before = models.TextField()
    template_body_after = models.TextField()
    Status = models.CharField(max_length=10, default = 'Active')
    CreatedDateTime = models.DateTimeField(auto_now_add = True)
    LastUpdatedDateTime = models.DateTimeField(auto_now = True)
    CCTO = models.EmailField(blank=True, null=True)
    signatures = models.CharField(max_length = 200)
    def __str__(self):
        return self.TemplateName 

from django.db import models
from myusersession.models import CompanyUser

class NewCountryCode(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    company_id = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, default=1, related_name="company_id",limit_choices_to={'company_admin': True})
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company_id', 'code'], name='unique_user_company_code')
        ]
    def __str__(self):
        return self.name
from django.db import models
from myusersession.models import CompanyUser

class CountryCode(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    user_id = models.ForeignKey(CompanyUser, on_delete=models.CASCADE, default=2)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'code'], name='unique_user_company_code')
        ]
    def __str__(self):
        return self.name
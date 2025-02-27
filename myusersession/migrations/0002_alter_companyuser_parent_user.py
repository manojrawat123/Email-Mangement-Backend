# Generated by Django 4.0.3 on 2024-07-05 08:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myusersession', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyuser',
            name='parent_user',
            field=models.ForeignKey(blank=True, limit_choices_to={'company_admin': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to=settings.AUTH_USER_MODEL),
        ),
    ]

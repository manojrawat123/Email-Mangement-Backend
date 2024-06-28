# Generated by Django 4.0.3 on 2024-06-28 07:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myusersession', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyuser',
            name='parent_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to=settings.AUTH_USER_MODEL),
        ),
    ]

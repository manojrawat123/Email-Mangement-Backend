# Generated by Django 4.0.3 on 2024-06-28 07:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myusersession', '0003_alter_companyuser_parent_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyuser',
            name='parent_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to=settings.AUTH_USER_MODEL),
        ),
    ]

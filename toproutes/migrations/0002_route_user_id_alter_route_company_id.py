# Generated by Django 4.0.3 on 2024-07-03 11:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('toproutes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='route_user_id', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='route',
            name='company_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='route_company_id', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 4.0.3 on 2024-07-03 08:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companycustomer', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorRateTabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_rate_name', models.CharField(max_length=200, unique=True)),
                ('vendor_prefix', models.CharField(max_length=200, unique=True)),
                ('created_date', models.DateField(auto_now=True)),
                ('rate_status', models.BooleanField(default=True)),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companycustomer.customer')),
                ('vendor_rate_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management_profile.managementprofilename')),
            ],
        ),
    ]

# Generated by Django 4.0.3 on 2024-06-24 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management_profile', '0001_initial'),
        ('companycustomer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerRateTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate_name', models.CharField(max_length=255)),
                ('customer_prefix', models.CharField(max_length=200)),
                ('created_date', models.DateField(default=django.utils.timezone.now)),
                ('rate_status', models.CharField(max_length=20)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companycustomer.customer')),
                ('rate_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management_profile.managementprofilename')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='customerratetable',
            constraint=models.UniqueConstraint(fields=('user_id', 'rate_name'), name='unique_user_rate'),
        ),
        migrations.AddConstraint(
            model_name='customerratetable',
            constraint=models.UniqueConstraint(fields=('user_id', 'customer_prefix'), name='unique_user_customer_prefix'),
        ),
    ]

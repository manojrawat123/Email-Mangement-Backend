# Generated by Django 4.0.3 on 2024-07-03 08:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer_rate', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RateTabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_code', models.CharField(max_length=100)),
                ('country_name', models.CharField(max_length=255)),
                ('rate', models.DecimalField(decimal_places=4, max_digits=10)),
                ('billing_increment_1', models.IntegerField()),
                ('billing_increment_n', models.IntegerField()),
                ('status', models.CharField(default='active', max_length=20)),
                ('effective_date', models.DateField()),
                ('created_date', models.DateField(default=django.utils.timezone.now)),
                ('rate_status', models.CharField(max_length=20)),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('customer_rate_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer_rate.customerratetable')),
            ],
        ),
    ]

# Generated by Django 4.0.3 on 2023-10-16 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
        ('emaillog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emaillog',
            name='CompanyID',
        ),
        migrations.AddField(
            model_name='emaillog',
            name='CustomerId',
            field=models.ManyToManyField(to='customer.customer'),
        ),
    ]

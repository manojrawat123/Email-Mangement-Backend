# Generated by Django 4.0.3 on 2024-06-18 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]

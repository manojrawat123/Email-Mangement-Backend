# Generated by Django 4.0.3 on 2024-06-19 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0003_customer_active'),
        ('invoice', '0002_alter_invoice_active_alter_invoice_invoice_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dispute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dispute_type', models.CharField(choices=[('IN', 'In'), ('OUT', 'Out')], max_length=3)),
                ('dispute_number', models.CharField(max_length=20, unique=True)),
                ('dispute_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('desc', models.TextField()),
                ('active', models.BooleanField(default=True)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('invoice_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.invoice')),
            ],
        ),
    ]

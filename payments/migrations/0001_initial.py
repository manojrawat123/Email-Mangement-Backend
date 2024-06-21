# Generated by Django 4.0.3 on 2024-06-21 06:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0003_customer_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(choices=[('IN', 'In'), ('OUT', 'Out')], max_length=50)),
                ('payment_date', models.DateField()),
                ('payment_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bank_charges', models.DecimalField(decimal_places=2, max_digits=10)),
                ('other_charges', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('payment_mode', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
            ],
        ),
    ]

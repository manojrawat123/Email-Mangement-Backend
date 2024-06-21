# Generated by Django 4.0.3 on 2024-06-21 07:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('top_route_name', models.CharField(max_length=255)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('destination', models.CharField(max_length=255)),
                ('profile', models.CharField(max_length=255)),
                ('rate', models.DecimalField(decimal_places=10, max_digits=10)),
                ('asr', models.CharField(max_length=50)),
                ('acd', models.CharField(max_length=50)),
                ('increment', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
    ]

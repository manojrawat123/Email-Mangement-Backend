# Generated by Django 4.0.3 on 2024-06-12 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailtemplate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailtemplate',
            name='template_body_after',
            field=models.TextField(default='Template After Message'),
        ),
        migrations.AddField(
            model_name='emailtemplate',
            name='template_body_before',
            field=models.TextField(default='Template Before Message'),
        ),
    ]

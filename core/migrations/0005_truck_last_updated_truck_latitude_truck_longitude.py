# Generated by Django 5.1.5 on 2025-02-13 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_route'),
    ]

    operations = [
        migrations.AddField(
            model_name='truck',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='truck',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='truck',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]

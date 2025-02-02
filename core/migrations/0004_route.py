# Generated by Django 5.1.5 on 2025-02-02 14:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_driver_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.CharField(editable=False, max_length=6, primary_key=True, serialize=False, unique=True)),
                ('start_location', models.CharField(max_length=100)),
                ('end_location', models.CharField(max_length=100)),
                ('distance_km', models.FloatField(help_text='Distance in kilometers', validators=[django.core.validators.MinValueValidator(0.0)])),
                ('estimated_fuel_cost', models.DecimalField(decimal_places=2, help_text='Estimated cost in currency', max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Route',
                'verbose_name_plural': 'Routes',
                'ordering': ['-created_at'],
            },
        ),
    ]

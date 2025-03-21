# Generated by Django 5.1.5 on 2025-02-01 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='id',
            field=models.CharField(editable=False, max_length=6, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='id',
            field=models.CharField(editable=False, max_length=6, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='truck',
            name='id',
            field=models.CharField(editable=False, max_length=6, primary_key=True, serialize=False, unique=True),
        ),
    ]

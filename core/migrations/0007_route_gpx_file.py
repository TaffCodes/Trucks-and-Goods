# Generated by Django 5.1.5 on 2025-02-15 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_trip_destination_trip_route'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='gpx_file',
            field=models.FileField(blank=True, null=True, upload_to='gpx_files/'),
        ),
    ]

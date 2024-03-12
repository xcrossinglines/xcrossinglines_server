# Generated by Django 4.1.7 on 2023-11-11 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0008_alter_job_extra_discount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='description',
            field=models.IntegerField(blank=True, choices=[(0, 'Pickup'), (1, 'Dropoff'), (2, 'Both')], default=0, null=True),
        ),
    ]

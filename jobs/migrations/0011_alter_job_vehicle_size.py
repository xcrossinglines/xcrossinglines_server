# Generated by Django 4.1.7 on 2024-03-12 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0010_alter_route_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='vehicle_size',
            field=models.FloatField(blank=True, choices=[(1.0, '1.0 Ton'), (1.5, '1.5 Ton'), (2.0, '2.0 Ton'), (3.0, '3.0 Ton'), (4.0, '4.0 Ton'), (8.0, '8.0 Ton')], default=1.0, null=True),
        ),
    ]
# Generated by Django 4.1.7 on 2023-10-11 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QuoteRoutes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('route_name', models.CharField(blank=True, default='', max_length=400, null=True)),
                ('lat', models.DecimalField(blank=True, decimal_places=30, max_digits=35, null=True)),
                ('lng', models.DecimalField(blank=True, decimal_places=30, max_digits=35, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuoteJob',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('helpers', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3)], default=1, null=True)),
                ('floors', models.IntegerField(blank=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=0, null=True)),
                ('shuttle', models.IntegerField(blank=True, choices=[(0, 'None'), (1, 'Pick up'), (2, 'Drop off'), (3, 'both')], default=0, null=True)),
                ('vehicle_size', models.FloatField(blank=True, choices=[(1.0, '1.0 Ton'), (1.5, '1.5 Ton'), (4.0, '4.0 Ton'), (8.0, '8.0 Ton')], default=1.0, null=True)),
                ('payment_option', models.CharField(blank=True, choices=[('EFT', 'EFT'), ('CASH', 'CASH')], default='CASH', max_length=50, null=True)),
                ('distance', models.FloatField(blank=True, default=0.0, null=True)),
                ('driver_note', models.TextField(blank=True, default='', max_length=1000, null=True)),
                ('base_fee', models.FloatField(blank=True, default=0.0, null=True)),
                ('amount_due', models.FloatField(blank=True, default=0.0, null=True)),
                ('mid_discount', models.FloatField(blank=True, default=0.0, null=True)),
                ('job_date', models.DateField(null=True)),
                ('job_time', models.TimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('routes', models.ManyToManyField(blank=True, to='quotejobs.quoteroutes')),
            ],
        ),
    ]

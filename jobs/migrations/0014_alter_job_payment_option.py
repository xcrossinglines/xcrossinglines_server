# Generated by Django 4.1.7 on 2023-06-03 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0013_alter_job_hear_about_us'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='payment_option',
            field=models.CharField(blank=True, choices=[('EFT', 'EFT'), ('CASH', 'CASH')], default='CASH', max_length=50, null=True),
        ),
    ]
